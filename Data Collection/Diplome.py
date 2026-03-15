import pandas as pd
import os
from datetime import datetime

# المسارات
output_folder = "Data Clean"
os.makedirs(output_folder, exist_ok=True)

print("🚀 إنشاء بيانات التعليم والطلبة (2021-2024)...")

# البيانات من "Le Maroc en chiffres 2025" صفحة 34
data = {
    'Année': [2021, 2022, 2023, 2024],
    
    # Effectifs dans l'enseignement supérieur
    'Effectif_Supérieur': [1095668, 1106225, 1118000, 1125000],
    
    # Nouveaux diplômés chaque année (estimation)
    'Nouveaux_Diplômés': [145000, 148000, 151000, 153000],
    
    # Effectifs par niveau
    'Effectif_Primaire': [3765221, 3765221, 3710000, 3606526],
    'Effectif_Collège': [1840393, 1918691, 1990000, 2153931],
    'Effectif_Lycée': [1050535, 1096386, 1140000, 1243349],
    
    # Taux de réussite (approximatif)
    'Taux_Réussite_Bac': [62.3, 63.1, 64.2, 65.0]
}

df = pd.DataFrame(data)

# ✅ التعديل ديالك: تقسيم الخريجين
df['Diplomes_Univ'] = df['Nouveaux_Diplômés'] * 0.7  # الجامعة (70%)
df['Diplomes_Formation_Pro'] = df['Nouveaux_Diplômés'] * 0.3  # التكوين المهني (30%)

# حساب إجمالي الطلبة
df['Total_Élèves'] = (df['Effectif_Primaire'] + df['Effectif_Collège'] + 
                      df['Effectif_Lycée'] + df['Effectif_Supérieur'])

# إضافة معلومات
df['Source'] = "Ministère Education Nationale / HCP"
df['Date_extraction'] = datetime.now().strftime("%Y-%m-%d")

# حفظ الملف
output_file = os.path.join(output_folder, "03_diplomes_2021_2024.csv")
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n✅ تم إنشاء ملف التعليم!")
print(f"📁 الملف: {output_file}")
print("\n📋 البيانات الأساسية:")
print(df[['Année', 'Effectif_Supérieur', 'Nouveaux_Diplômés', 
          'Diplomes_Univ', 'Diplomes_Formation_Pro', 'Total_Élèves']].to_string(index=False))

# إحصائيات سريعة
print("\n📈 إحصائيات (2021-2024):")
print(f"   مجموع الخريجين الجدد: {df['Nouveaux_Diplômés'].sum():,}")
print(f"   - خريجي الجامعات: {df['Diplomes_Univ'].sum():,.0f}")
print(f"   - خريجي التكوين المهني: {df['Diplomes_Formation_Pro'].sum():,.0f}")