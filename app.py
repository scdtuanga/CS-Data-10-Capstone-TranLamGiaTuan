import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from utils.analysis import monthly_sales, top_by_category
from utils.ai_helper import analyze_with_ai

os.makedirs("reports", exist_ok=True)
os.makedirs("charts", exist_ok=True)
chart_path = os.path.join("charts", "chart.png")

st.title("Phân tích dữ liệu & Báo cáo tự động")

uploaded_file = st.file_uploader("Tải lên file CSV hoặc Excel", type=["csv", "xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Xem trước dữ liệu")
    st.dataframe(df.head())

    st.write("Các cột trong dữ liệu:", df.columns.tolist())

    date_col = st.selectbox("Chọn cột ngày", df.columns)

    numeric_cols = df.select_dtypes("number").columns
    if len(numeric_cols) == 0:
        st.error("Không có cột số nào để phân tích.")
        st.stop()
    value_col = st.selectbox("Chọn cột giá trị", numeric_cols)

    category_cols = df.select_dtypes("object").columns
    category_col = st.selectbox("Chọn cột danh mục", category_cols) if len(category_cols) > 0 else None

    try:
        monthly = monthly_sales(df.copy(), value_col, date_col)
        st.subheader("Tổng hợp theo tháng")
        st.dataframe(monthly)

        if monthly.empty or monthly[value_col].isna().all():
            st.warning(" Không có dữ liệu để vẽ biểu đồ.")
        else:
            fig, ax = plt.subplots()
            ax.plot(monthly["Month"].astype(str), monthly[value_col], marker="o", linestyle="-")
            ax.set_title(f"Xu hướng {value_col} theo tháng")
            ax.set_xlabel("Tháng")
            ax.set_ylabel(value_col)
            plt.xticks(rotation=45)
            plt.tight_layout()

            fig.savefig(chart_path)
            st.pyplot(fig)
            plt.close(fig)

        if category_col:
            top5 = top_by_category(df.copy(), value_col, category_col)
            st.subheader(f"Top theo {category_col}")
            st.dataframe(top5)
        else:
            top5 = pd.DataFrame()

        excel_path = os.path.join("reports", "report.xlsx")
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="RawData", index=False)
            monthly.to_excel(writer, sheet_name="MonthlyData", index=False)
            if not top5.empty:
                top5.to_excel(writer, sheet_name=f"Top_{category_col}", index=False)

        with open(excel_path, "rb") as f:
            st.download_button("Tải báo cáo Excel", f.read(), file_name="report.xlsx")

        if os.path.exists(chart_path):
            with open(chart_path, "rb") as f:
                st.download_button("Tải biểu đồ PNG", f.read(), file_name="chart.png")

        st.subheader("Phân tích chi tiết & Giải pháp (AI)")
        summary_text = f"Tổng hợp theo tháng:\n{monthly.to_string(index=False)}"
        if not top5.empty:
            summary_text += f"\n\nTop {category_col}:\n{top5.to_string(index=False)}"
        ai_report = analyze_with_ai(summary_text)
        st.write(ai_report)

    except Exception as e:
        st.error(f"Lỗi khi phân tích dữ liệu: {e}")
