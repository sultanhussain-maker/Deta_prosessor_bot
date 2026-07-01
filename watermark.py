# app/core/watermark.py
def add_watermark_excel(df, watermark):
    df["_WATERMARK_"] = watermark
    return df