# app/main.py
import streamlit as st
from database import get_db_connection

# Import tab modules
from bom_tab import show_bom_tab
from materials_tab import show_materials_tab
from construction_tab import show_construction_tab
from lab_samples_tab import show_lab_samples_tab
from manual_entry_tab import show_manual_entry_tab
from export_tab import show_export_tab

# Page config
st.set_page_config(page_title="🔧 Multi-Tab BOM Tool", layout="wide")
st.title("🔧 Modular BOM & Data Manager")

# Connect to DB
conn = get_db_connection()

# Tabs UI
tab_bom, tab_materials, tab_construction, tab_lab, tab_manual_entry, show_export = st.tabs([
    "📦 Bill of Materials",
    "🧪 Engineering Materials",
    "🏗️ Construction Quantities",
    "🧬 Lab Sample Tracker",
    "🧮 Manual Entry",
    "📤 Export Tables"
])

# Show each tab content
with tab_bom:
    show_bom_tab(conn)

with tab_materials:
    show_materials_tab(conn)

with tab_construction:
    show_construction_tab(conn)

with tab_lab:
    show_lab_samples_tab(conn)

with tab_manual_entry:
    show_manual_entry_tab(conn)
# Inside your tab selector:
with show_export:
    show_export_tab(conn)

# Footer
st.markdown("-----")
st.markdown("Built with ❤️ using Streamlit + DuckDB")