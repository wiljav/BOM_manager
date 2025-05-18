# app/bom_tab.py

import streamlit as st
import pandas as pd

def show_bom_tab(conn):
    st.subheader("📦 Bill of Materials")
    st.write("Upload or manage parts used in mechanical assemblies.")
    st.write("This tab allows you to upload a CSV file containing the Bill of Materials (BOM) data.")
    st.write("The BOM should include columns like Part Number, Description, Quantity, and Unit Cost.")
    st.write("You can also add new parts directly through the form below.")
    st.write("Ensure your CSV file is formatted correctly to avoid errors during upload.")
    st.write("You can view the uploaded BOM in the table below.")
    st.write("Please ensure that the data is accurate to maintain project integrity.")
    
    
    from utils import process_csv_upload
    process_csv_upload(conn, "BOM")
