import pandas as pd

def monthly_sales(df, value_col, date_col):
    # Ép kiểu số cho cột giá trị
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    # Parse ngày tự động, không chỉ định format
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    # Lọc dữ liệu hợp lệ
    clean = df[[date_col, value_col]].dropna()
    if clean.empty:
        return pd.DataFrame(columns=["Month", value_col])
    clean["Month"] = clean[date_col].dt.to_period("M")
    monthly = clean.groupby("Month", as_index=False)[value_col].sum()
    return monthly.sort_values("Month")

def top_by_category(df, value_col, category_col, n=5):
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    return (
        df.groupby(category_col)[value_col]
        .sum()
        .reset_index()
        .sort_values(value_col, ascending=False)
        .head(n)
    )