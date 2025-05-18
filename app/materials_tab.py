# app/materials_tab.py

import streamlit as st
import pandas as pd

def show_materials_tab(conn):
    st.subheader("🧪 Engineering Materials")
    st.write("Upload or manage engineering materials used in projects.")
    st.write("This tab allows you to upload a CSV file containing material data.")
    st.write("The materials data should include columns like Material ID, Description, Quantity, and Unit Cost.")
    st.write("Ensure your CSV file is formatted correctly to avoid errors during upload.")
    st.write("You can also add new materials directly through the form below.")
    st.write("Please ensure that the data is accurate to maintain project integrity.")
    st.write("You can view the uploaded materials in the table below.")

    from utils import process_csv_upload
    process_csv_upload(conn, "Materials")
