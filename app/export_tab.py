import streamlit as st
import duckdb
import pandas as pd
from io import BytesIO

def show_export_tab(conn):
    st.title("📤 Export Tables to Excel")

    tables = conn.execute("SHOW TABLES").fetchdf()
    table_names = tables['name'].tolist()

    if not table_names:
        st.warning("No tables found in the database.")
        return

    selected_table = st.selectbox("Select a table to export", table_names)

    if selected_table:
        df = conn.execute(f'SELECT * FROM "{selected_table}"').fetchdf()
        st.dataframe(df, use_container_width=True)

        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, engine="openpyxl")
        excel_buffer.seek(0)

        st.download_button(
            label=f"⬇️ Download '{selected_table}' as Excel",
            data=excel_buffer,
            file_name=f"{selected_table}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"download_{selected_table}"
        )
