# PoE2 Autonomous DPS Engine & Agent Guild

Bu proje, Path of Exile 2 (PoE2) için tamamen kapalı devre çalışan, PoE1 legacy mekaniklerinden arındırılmış otonom bir DPS simülasyon motorudur.

## Ajan Hiyerarşisi
* **Sistem Mimarı:** PoE2 izolasyonunu ve şema bütünlüğünü denetler.
* **Orchestrator:** Ajan iş akışını ve GitHub Actions hattını yönetir.
* **Ajan 1 (Data Parser):** Canlı PoE2 verilerini çeker ve temizler.
* **Uzman Ajanlar (Martial / Arcane / Spirit):** Yetenek ve destek taşı etiket uyumunu denetler.
* **Ajan 3 (PoB Calc Engine):** `CalcOffence.lua` mantığıyla DPS hesaplar.
* **Ajan 4 (Executioner):** Rapor oluşturup repoya işler.
