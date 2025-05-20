# app/utils.py

import duckdb
import os
import pandas as pd
import streamlit as st
import hashlib
import uuid
from io import BytesIO


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

            # button_suffix = str(uuid.uuid4())

            # Download Excel
            st.subheader("Export to Excel")
            st.write("You can export the uploaded data to an Excel file.")
            if not df.empty:
                excel_buffer = BytesIO()
                df.to_excel(excel_buffer, index=False, engine="openpyxl")
                excel_buffer.seek(0)

                st.download_button(
                    label="⬇️ Download Excel File",
                    data=excel_buffer,
                    file_name=f"{table_name}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"download_{table_name}"
                )
                st.write("The Excel file has been created. Click the button to download it.")
                st.success(f"✅ Exported '{table_name}' to Excel successfully.")
            else:
                st.warning("⚠️ Dataframe is empty. Upload and process a valid CSV.")
        # except pd.errors.ParserError:
            # st.error("❌ Error: The uploaded file is not a valid CSV. Please check the format.")
        # except duckdb.DuckDBException as e:
            # st.error(f"❌ Error: {e}")
        # except FileNotFoundError:
            # st.error("❌ Error: The file was not found. Please check the file path.")
        # except ValueError as e:
            # st.error(f"❌ Error: {e}")
        # except TypeError as e:
            # st.error(f"❌ Error: {e}")
        # except KeyError as e:
            # st.error(f"❌ Error: Missing column in the CSV file. Please check the headers.")
        # except pd.errors.EmptyDataError:
            # st.error("❌ Error: The uploaded CSV file is empty. Please upload a valid file.")
            # if df.empty:
                # st.error("❌ Error: The uploaded CSV file is empty.")
        # except pd.errors.DtypeWarning:
            # st.warning("⚠️ Warning: Some columns have mixed data types. Please check the data types.")
        # except duckdb.InvalidInputError as e:
            # st.error(f"❌ Error: Invalid input for DuckDB. Please check the data types.")
        # except duckdb.DatabaseError as e:
            # st.error(f"❌ Error: Database error occurred. Please check the database connection.")
        # except duckdb.ProgrammingError as e:
            # st.error(f"❌ Error: Programming error occurred. Please check the SQL syntax.")
        # except duckdb.DuckDBPyException as e:
            # st.error(f"❌ Error: DuckDB error occurred. Please check the SQL syntax.")
        # except duckdb.DuckDBException as e:
            # st.error(f"❌ Error: DuckDB error occurred. Please check the SQL syntax.")
        except Exception as e:
            st.error(f"❌ Error processing CSV: {e}")