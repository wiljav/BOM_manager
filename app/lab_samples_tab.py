# app/lab_samples_tab.py

import streamlit as st
import pandas as pd

def show_lab_samples_tab(conn):
    st.subheader("🧬 Lab Sample Tracker")
    st.write("Upload or manage lab samples used in engineering projects.")
    st.write("This tab allows you to upload a CSV file containing lab sample data.")
    st.write("The lab samples data should include columns like Sample ID, Description, Quantity, and Test Results.")
    st.write("Ensure your CSV file is formatted correctly to avoid errors during upload.")
    st.write("You can also add new lab samples directly through the form below.")
    st.write("Please ensure that the data is accurate to maintain project integrity.")
    st.write("You can view the uploaded lab samples in the table below.")

    # Reuse your shared CSV upload function
    from utils import process_csv_upload
    process_csv_upload(conn, "Lab Samples List")


    # lab_samples_data = pd.read_csv("lab_samples_data.csv")
    # st.dataframe(lab_samples_data)