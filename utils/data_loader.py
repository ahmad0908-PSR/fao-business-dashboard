# utils/data_loader.py

import pandas as pd
import streamlit as st

# ==========================================
# GOOGLE SHEET CONFIGURATION
# ==========================================

SHEET_ID = "1wQKemvbgAOeyzFkHSAzaY7PS23ljmHmuQNHs18vdpyk"

BUSINESS_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
    "/gviz/tq?tqx=out:csv&sheet=Businesses_DB"
)

PHASE_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
    "/gviz/tq?tqx=out:csv&sheet=Phase_Tracking"
)

SUMMARY_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
    "/gviz/tq?tqx=out:csv&sheet=Summary"
)


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data(ttl=300)
def load_data():
    """
    Loads all dashboard data from Google Sheets.

    Returns:
        business_df (DataFrame)
        phase_df (DataFrame)
        summary_df (DataFrame)
    """

    try:
        # Load sheets
        business_df = pd.read_csv(BUSINESS_URL)
        phase_df = pd.read_csv(PHASE_URL)
        summary_df = pd.read_csv(SUMMARY_URL)

        # Validate data
        if business_df.empty:
            st.warning("Businesses_DB sheet is empty.")

        if phase_df.empty:
            st.warning("Phase_Tracking sheet is empty.")

        if summary_df.empty:
            st.warning("Summary sheet is empty.")

        return business_df, phase_df, summary_df

    except Exception as e:
        st.error("❌ Failed to load data from Google Sheets")
        st.error(str(e))

        return (
            pd.DataFrame(),
            pd.DataFrame(),
            pd.DataFrame()
        )


# ==========================================
# OPTIONAL DEBUG FUNCTION
# ==========================================

def show_data_info():
    """
    Displays debugging information.
    Useful during development.
    """

    business_df, phase_df, summary_df = load_data()

    st.subheader("📊 Data Status")

    st.write("Business_DB Rows:", len(business_df))
    st.write("Phase_Tracking Rows:", len(phase_df))
    st.write("Summary Rows:", len(summary_df))

    st.write("Business Columns:", list(business_df.columns))
    st.write("Phase Columns:", list(phase_df.columns))
    st.write("Summary Columns:", list(summary_df.columns))
    st.write(BUSINESS_URL)