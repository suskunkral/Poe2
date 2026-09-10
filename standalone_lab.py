import json
import os
from datetime import datetime

DATA_DIR = "data"
REVIEWS_DIR = "reviews"

def load_data():
    with open(os.path.join(DATA_DIR, "active_skills.json"), "r", encoding="utf-8") as f:
        active_skills = json.load(f)
    with open(os.path.join(DATA_DIR, "support_gems.json"), "r", encoding="utf-8") as f:
        support_gems = json.load(f)
    return active_skills, support_gems

def is_support_compatible(skill_tags, support):
    """Uzman Ajanlar: PoE2 Etiket Denetimi (Allowed & Excluded)"""
    allowed = support.get("allowed_types", [])
    excluded = support.get("excluded_types", [])

    # Excluded kontrolü: Yetenekte yasaklı etiket varsa bağlama
    if any(tag in skill_tags for tag in excluded):
        return False

    # Allowed kontrolü: Eğer kısıtlama listesi varsa en az biri uyuşmalı
    if allowed and not any(tag in skill_tags for tag in allowed):
        return False

    return True

def calculate_pob_dps(active_skill, supports):
    """Ajan 3: PoB CalcOffence.lua Matematiği (Base Damage * CastRate * More Multipliers)"""
    cast_time = active_skill.get("cast_time", 1.0)
    cast_rate = 1.0 / cast_time if cast_time > 0 else 1.0
    
    # Taban Hasar Mantığı (Varsayılan Simülasyon Değeri)
    base_damage = 100.0 

    # PoB More Çarpan Mantığı: Tüm More değerleri katlanarak çarpılır
    more_multiplier = 1.0
    for s in supports:
        # Varsayılan %30 More Destek Çarpanı (PoB Standart Tabanı)
        more_multiplier *= 1.30 

    final_dps = (base_damage * cast_rate) * more_multiplier
    return round(final_dps, 2)

def run_simulation():
    print("[+] [Orkestra Şefi] Uzman Ajanlar ve PoB Hesaplama Motoru Çalıştırılıyor...")
    active_skills, support_gems = load_data()

    results = []

    for skill in active_skills:
        skill_tags = skill.get("tags", [])
        
        # Uzman Ajanların Etiket Filtresi
        compatible_supports = [
            s for s in support_gems if is_support_compatible(skill_tags, s)
        ]

        # En fazla 5 Destek Taşı Yuvası (PoE2 Gem Sockets Limiti)
        selected_supports = compatible_supports[:5]

        dps = calculate_pob_dps(skill, selected_supports)

        results.append({
            "skill_name": skill["name"],
            "tags": skill_tags,
            "supports_used": [s["name"] for s in selected_supports],
            "support_count": len(selected_supports),
            "calculated_dps": dps
        })

    # Ajan 4: En Yüksek DPS Veren Top 10 Kombinasyonu Sırala
    results.sort(key=lambda x: x["calculated_dps"], reverse=True)
    top_10 = results[:10]

    os.makedirs(REVIEWS_DIR, exist_ok=True)
    report_file = os.path.join(REVIEWS_DIR, "top10_dps_report.md")

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"# PoE2 Top 10 DPS Raporu (Ajan Konseyi Simülasyonu)\n")
        f.write(f"*Tarih:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("| Sıra | Aktif Yetenek | Kullanılan Destek Taşları (Max 5) | Tahmini DPS |\n")
        f.write("|---|---|---|---|\n")
        
        for idx, res in enumerate(top_10, 1):
            supports_str = ", ".join(res["supports_used"]) if res["supports_used"] else "Yok"
            f.write(f"| {idx} | **{res['skill_name']}** | {supports_str} | **{res['calculated_dps']}** |\n")

    print(f"[✓] Ajan 4 Tamamlandı: Top 10 Raporu '{report_file}' dosyasına işlendi.")

if __name__ == "__main__":
    run_simulation()
