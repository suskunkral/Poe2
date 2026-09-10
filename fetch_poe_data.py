import os
import json
import urllib.request

# Veri Depolama Dizinleri
DATA_DIR = "data"
REPOE_GEMS_URL = "https://repoe-fork.github.io/pob-data/poe2/gems.json"

# PoE1 Yasaklı Terimler Listesi (Mimar Güvenlik Katmanı)
BANNED_KEYS = ["socket_colour", "linked", "fusing", "links", "item_type"]

def validate_poe2_schema(data_dict):
    """PoE1 verilerini ve yasaklı parametreleri süzerek temizler."""
    cleaned = {}
    for key, value in data_dict.items():
        if any(banned in key for banned in BANNED_KEYS):
            continue
        cleaned[key] = value
    return cleaned

def fetch_and_parse_poe2_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    print("[+] [Mimar & Şef] GitHub Üzerinden Canlı PoE2 Verisi Çekiliyor...")

    try:
        # Doğrudan canlı siteden veriyi çek
        req = urllib.request.Request(REPOE_GEMS_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            raw_gems = json.loads(response.read().decode('utf-8'))

        print(f"[✓] Ham Gems Verisi Başarıyla İndirildi. Toplam Kayıt: {len(raw_gems)}")

        active_skills = []
        support_gems = []

        for gem_id, gem_data in raw_gems.items():
            clean_gem = validate_poe2_schema(gem_data)
            
            gem_name = clean_gem.get("name", gem_id)
            is_support = clean_gem.get("is_support", False)
            tags = clean_gem.get("tags", [])

            if is_support:
                support_gems.append({
                    "id": gem_id,
                    "name": gem_name,
                    "allowed_types": clean_gem.get("allowed_types", []),
                    "excluded_types": clean_gem.get("excluded_types", []),
                    "support_stats": clean_gem.get("stats", {})
                })
            else:
                active_skills.append({
                    "id": gem_id,
                    "name": gem_name,
                    "tags": tags,
                    "cast_time": clean_gem.get("cast_time", 1.0),
                    "base_damage": clean_gem.get("base_damage", {})
                })

        # Temiz PoE2 Verilerini Kaydet
        with open(os.path.join(DATA_DIR, "active_skills.json"), "w", encoding="utf-8") as f:
            json.dump(active_skills, f, ensure_ascii=False, indent=2)

        with open(os.path.join(DATA_DIR, "support_gems.json"), "w", encoding="utf-8") as f:
            json.dump(support_gems, f, ensure_ascii=False, indent=2)

        print(f"[✓] Ajan 1 Tamamlandı: {len(active_skills)} Aktif Yetenek, {len(support_gems)} Destek Taşı işlendi.")

    except Exception as e:
        print(f"[-] Veri çekme hatası: {e}")

if __name__ == "__main__":
    fetch_and_parse_poe2_data()
