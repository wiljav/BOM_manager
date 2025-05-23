# app/manual_entry_tab.py

import streamlit as st
import duckdb
import pandas as pd

def show_manual_entry_tab(conn):
    st.markdown("### 🧮 Manual Data Entry")
    st.write("Enter data below and submit to store it in the database.")

    with st.form("manual_data_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Name")
            description = st.text_area("Description", height=100)
            
            st.markdown("### Material and Quantity")
            st.markdown("Fill in the material and quantity details below.")
            material = st.text_input("Material")
            unit = st.text_input("Unit", value="pcs")

            st.markdown("### Note: The unit for quantity is set to 'pcs' by default.")
            quantity = st.number_input("Quantity", min_value=1, value=1)

        with col2:
            st.markdown("### Mass Value and Unit")
            st.markdown("Fill in the mass value and unit below.")
            mass_value = st.number_input("Mass Value", value=0.0, step=0.1)
            mass_unit = st.text_input("Mass Unit", value="kg")
            st.markdown("### Project Extra")
            st.markdown("Fill in the project extra value below.")
            project_extra = st.number_input("Project Extra", value=0.0, step=0.1)

        submitted = st.form_submit_button("➕ Add to Database")

        if submitted:
            try:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO parts (
                        name, quantity, unit_pcs, material, mass_value_eur, mass_unit_kg, project_extra_eur, description
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, quantity, unit, material, mass_value, mass_unit, project_extra, description))
                conn.commit()
                st.success("✅ Data successfully added to database!")
            except Exception as e:
                st.error(f"❌ Error saving data: {e}")

    # --- DOWNLOAD BUTTON ---
    if st.button("📥 Export Manual Entries to Excel", key="export_manual_excel"):
        try:
            df_export = conn.execute("SELECT * FROM parts ORDER BY id DESC").fetchdf()

            excel_file = "parts.xlsx"
            df_export.to_excel(excel_file, index=False, engine='openpyxl')

            with open(excel_file, "rb") as f:
                st.download_button(
                    label="⬇️ Download Excel File",
                    data=f,
                    file_name=excel_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_manual_excel"
                )
        except Exception as e:
            st.error(f"❌ Error exporting data: {e}")

    # --- PREVIEW DATA ---
    if st.checkbox("Show Current Data", key="show_manual_data"):
        try:
            df = conn.execute("SELECT * FROM parts ORDER BY id DESC LIMIT 10").fetchdf()
            st.dataframe(df, use_container_width=True)
            st.markdown("### Data Preview")
            st.markdown("This table shows the most recent manual entries along with their creation timestamps.")
            st.markdown("### Note: The timestamps indicate when each entry was created.")
        except:
            st.info("No data found yet.")