# app/construction_tab.py

import streamlit as st
from utils import process_csv_upload

def show_construction_tab(conn):
    st.subheader("🏗️ Construction Quantities")
    st.write("Upload or manage construction quantities and materials used in projects.")
    st.write("This tab allows you to upload a CSV file containing construction data.")
    st.write("The CSV should include columns like Material Type, Quantity, Unit Cost, and Project ID.")
    st.write("Ensure your CSV file is formatted correctly to avoid errors during upload.")
    st.write("You can also add new materials directly through the form below.")
    st.write("Please ensure that the data is accurate to maintain project integrity.")
    
    process_csv_upload(conn, "Construction Materials")