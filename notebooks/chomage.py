import pandas as pd
import os
from datetime import datetime

# المسارات
input_file = r"C:\Users\meriem\Desktop\Recrutment\Data Collection\Taux de chômage selon le diplôme au niveau national - Annuel.xlsx"
output_folder = "Data Clean"
os.makedirs(output_folder, exist_ok=True)

print("🚀 بداية معالجة بيانات البطالة...")

try:
    # 1. قراءة البيانات
    df = pd.read_excel(input_file, sheet_name='Annuel', skiprows=21)
    
    # 2. 📌 طباعة أسماء الأعمدة الموجودة فعلياً
    print("\n📊 أسماء الأعمدة في الملف:")
    for i, col in enumerate(df.columns):
        print(f"   {i}: '{col}'")
    
    # 3. إعادة تسمية الأعمدة بناءً على عددها
    if len(df.columns) == 6:
        df.columns = ['Col0', 'Année', 'Sans_diplôme', 'Niveau_moyen', 'Niveau_supérieur', 'Total_National']
        df = df.drop(columns=['Col0'])  # حذف العمود الفاضي
    else:
        # إذا كان عدد الأعمدة مختلف، نحتفظ بأسمائها الأصلية
        print(f"\n⚠️ عدد الأعمدة {len(df.columns)} غير متوقع. استخدام الأسماء الأصلية...")
    
    # 4. تنظيف البيانات
    df = df.dropna(subset=['Année']).copy()
    
    # 5. تحويل السنوات إلى أرقام
    df['Année'] = pd.to_numeric(df['Année'], errors='coerce')
    
    # 6. تصفية السنوات 2021-2024
    annees_voulues = [2021, 2022, 2023, 2024]
    df_final = df[df['Année'].isin(annees_voulues)].copy()
    
    if len(df_final) == 0:
        print("\n⚠️ لم يتم العثور على السنوات، البحث كنص...")
        # تجربة البحث كنص
        annees_str = [str(a) for a in annees_voulues]
        mask = df['Année'].astype(str).str.strip().isin(annees_str)
        df_final = df[mask].copy()
        df_final['Année'] = pd.to_numeric(df_final['Année'], errors='coerce')
    
    # 7. تحويل أرقام البطالة
    for col in ['Sans_diplôme', 'Niveau_moyen', 'Niveau_supérieur', 'Total_National']:
        if col in df_final.columns:
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce')
    
    # 8. إضافة معلومات
    df_final['Source'] = "Enquête Emploi, HCP"
    df_final['Date_extraction'] = datetime.now().strftime("%Y-%m-%d")
    
    # 9. حفظ الملف
    output_file = os.path.join(output_folder, "01_chomage_2021_2024.csv")
    df_final.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    # 10. عرض النتيجة
    print("\n" + "="*60)
    print("✅ تمت المعالجة بنجاح!")
    print("="*60)
    print(f"📁 الملف الناتج: {output_file}")
    print(f"📊 السنوات الموجودة: {sorted(df_final['Année'].unique())}")
    
    if len(df_final) > 0:
        print("\n📋 البيانات المستخرجة:")
        print(df_final[['Année', 'Sans_diplôme', 'Niveau_moyen', 'Niveau_supérieur', 'Total_National']].to_string(index=False))
    else:
        print("\n❌ لم يتم العثور على بيانات للسنوات 2021-2024")
        print("جميع السنوات في الملف:")
        print(sorted(df['Année'].dropna().unique()))
    
except Exception as e:
    print(f"❌ خطأ: {e}")
    import traceback
    traceback.print_exc()