# app/core/report.py
def generate_report(df):
    summary = df.describe(include="all").to_string()
    return f"📊 گزارش فایل:\n\nردیف‌ها: {len(df)}\nستون‌ها: {len(df.columns)}\n\n{summary}"