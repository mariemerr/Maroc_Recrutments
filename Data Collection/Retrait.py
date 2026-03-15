import pandas as pd
import os
from datetime import datetime

# المسارات
output_folder = "Data Clean"
os.makedirs(output_folder, exist_ok=True)

print("🚀 إنشاء بيانات التقاعد الحقيقية (2021-2024)...")

# البيانات الحقيقية من الصفحة 20-21
data = {
    'Année': [2021, 2022, 2023, 2024],
    'Départs_Total': [14722, 14654, 14195, 13689],
    'Education_Nationale': [6485, 6013, 5717, 4939],
    'Enseignement_Supérieur': [984, 974, 1020, 968],
    'Intérieur': [2986, 3257, 3260, 3353],
    'Santé': [1233, 1176, 1078, 1142],
    'Justice': [440, 464, 450, 466],
    'Economie_Finances': [418, 384, 416, 390]
}

df = pd.DataFrame(data)
df['Source'] = "Rapport RH 2026, p.20-21"
df['Date_extraction'] = datetime.now().strftime("%Y-%m-%d")

output_file = os.path.join(output_folder, "02_retraites_REAL_2021_2024.csv")
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n✅ تم إنشاء ملف التقاعد الحقيقي!")
print(f"📁 الملف: {output_file}")
print(df)