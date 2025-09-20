import pandas as pd
import json
from openpyxl import load_workbook
from datetime import datetime

# JSON oku
with open("data.json", "r", encoding="utf-8") as f:
    araclar = json.load(f)
plaka_to_id = {item["plaka"]: item["id"] for item in araclar}

# pandas ile oku (sadece veri için)
df = pd.read_excel("Kitap1.xlsx")

# Hesaplama fonksiyonu
def calculate(arac_id, tarih):
    mesai_ici = arac_id * 10
    mesai_disi = arac_id * 5
    return mesai_ici, mesai_disi

# openpyxl workbook
wb = load_workbook("Kitap1.xlsx")
ws = wb.active

# Satırları gez
for idx, row in df.iterrows():
    plaka = row["Plaka"]
    tarih = row["Tarih"]

    # Tarihi datetime nesnesine çevir (gün.ay.yıl formatı)
    if isinstance(tarih, str):
        try:
            tarih = datetime.strptime(tarih, "%d.%m.%Y")
        except ValueError:
            print(f"Uyarı: Satır {idx+2} tarih formatı hatalı: {tarih}")
            continue

    arac_id = plaka_to_id.get(plaka)
    if not arac_id:
        print(f"Uyarı: Satır {idx+2} için plaka bulunamadı: {plaka}")
        continue

    mesai_ici, mesai_disi = calculate(arac_id, tarih)

    # B kolonu (2. kolon) mesai içi, C kolonu (3. kolon) mesai dışı
    ws.cell(row=idx+2, column=2, value=mesai_ici)
    ws.cell(row=idx+2, column=3, value=mesai_disi)

wb.save("revize.xlsx")
print("Revize dosya kaydedildi.")
