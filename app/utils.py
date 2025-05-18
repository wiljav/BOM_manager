# app/utils.py

import duckdb
import os
import pandas as pd
import streamlit as st
import hashlib
import uuid

def process_csv_upload(conn, section_name):
    unique_table_suffix = str(uuid.uuid4())
    uploaded_file = st.file_uploader(f"Upload CSV for {section_name}", type="csv", key=f"csv_{section_name}")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, sep=";", encoding="utf-8")
            df.columns = [col.strip().replace('"', '').replace("'", "") for col in df.columns]

            # Generate unique table name
            sample_data = df.head().to_string().encode()
            unique_id = hashlib.md5(sample_data).hexdigest()[:8]
            base_name = os.path.splitext(uploaded_file.name)[0].replace(" ", "_")
            table_name = f"{base_name}_{unique_id}_{unique_table_suffix}"
            table_name = ''.join(c if c.isalnum() or c == '_' else '_' for c in table_name)

            # Clean column names
            cleaned_columns = [''.join(c if c.isalnum() or c == '_' else '_' for c in col) for col in df.columns]
            df.columns = cleaned_columns

            cur = conn.cursor()

            # Drop old table
            cur.execute(f'DROP TABLE IF EXISTS "{table_name}"')
            conn.execute("CHECKPOINT")

            # Recreate table
            columns_sql = []
            for col in df.columns:
                sample_value = df[col].iloc[0] if not df.empty else None
                if isinstance(sample_value, (int, bool)):
                    dtype = 'INTEGER'
                elif isinstance(sample_value, float):
                    dtype = 'FLOAT'
                else:
                    dtype = 'VARCHAR'

                columns_sql.append(f'"{col}" {dtype}')

            create_table_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({", ".join(columns_sql)})'
            cur.execute(create_table_sql)

            # Insert data
            cur.execute("BEGIN TRANSACTION;")
            for _, row in df.iterrows():
                values = tuple(row[col] for col in df.columns)
                placeholders = ", ".join("?" * len(values))
                cols_quoted = ', '.join(f'"{col}"' for col in df.columns)
                sql = f'INSERT INTO "{table_name}" ({cols_quoted}) VALUES ({placeholders})'
                cur.execute(sql, values)
            cur.execute("COMMIT;")

            st.success(f"✅ Created table `{table_name}` and inserted {len(df)} rows.")
            st.dataframe(df.head(), use_container_width=True)

            # Generate NEW unique suffix just for the button
            button_suffix = str(uuid.uuid4())

            # Download Excel
            if st.button(f"📥 Export '{table_name}' to Excel", key=f"export_{table_name}_{button_suffix}"):
                excel_file = f"{table_name}.xlsx"
                df.to_excel(excel_file, index=False, engine='openpyxl')
                with open(excel_file, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Excel File",
                        data=f,
                        file_name=excel_file,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"download_{table_name}_{button_suffix}"
                    )
                st.success(f"✅ Exported '{table_name}' to Excel successfully.")

        except Exception as e:
            st.error(f"❌ Error processing CSV: {e}")