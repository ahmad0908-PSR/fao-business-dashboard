import pandas as pd
import streamlit as st

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


@st.cache_data(ttl=300)
def load_data():
    try:
        business_df = pd.read_csv(BUSINESS_URL)
        phase_df = pd.read_csv(PHASE_URL)
        summary_df = pd.read_csv(SUMMARY_URL)

        # ✅ Strip ALL column name whitespace
        business_df.columns = business_df.columns.str.strip()
        phase_df.columns = phase_df.columns.str.strip()
        summary_df.columns = summary_df.columns.str.strip()

        if business_df.empty:
            st.warning("Businesses_DB sheet is empty.")
        if phase_df.empty:
            st.warning("Phase_Tracking sheet is empty.")
        if summary_df.empty:
            st.warning("Summary sheet is empty.")

        # ✅ Strip whitespace from key column values
        phase_df["Phase"] = phase_df["Phase"].str.strip()
        phase_df["Status"] = phase_df["Status"].str.strip()
        business_df["Business_ID"] = business_df["Business_ID"].str.strip()
        phase_df["Business_ID"] = phase_df["Business_ID"].str.strip()
        summary_df["Business_ID"] = summary_df["Business_ID"].str.strip()

        return business_df, phase_df, summary_df

    except Exception as e:
        st.error("❌ Failed to load data from Google Sheets")
        st.error(str(e))
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()


def build_phase_summary(phase_df, business_df, summary_df, phase_label):
    """
    Builds a summary-style DataFrame for a specific phase.

    For Phase 2: only includes businesses that have actual
    Phase 2 rows in phase_df — meaning they were explicitly
    added to Phase 2 tracking.

    For Phase 1: includes all businesses with Phase 1 rows.
    """

    phase_rows = phase_df[phase_df["Phase"] == phase_label].copy()

    if phase_rows.empty:
        return pd.DataFrame()

    # ✅ KEY FIX: For Phase 2, only include businesses that
    # actually have Phase 2 records in Phase_Tracking.
    # This naturally excludes businesses that are still in Phase 1
    # since they won't have any Phase 2 rows yet.
    biz_in_phase = phase_rows["Business_ID"].unique()

    def compute_completion(biz_id):
        rows = phase_rows[phase_rows["Business_ID"] == biz_id]
        total = len(rows)
        completed = rows[rows["Status"].str.lower() == "completed"].shape[0]
        return round((completed / total * 100), 1) if total > 0 else 0

    records = []
    for biz_id in biz_in_phase:
        biz_rows = phase_rows[phase_rows["Business_ID"] == biz_id]
        latest_stage = biz_rows.iloc[-1]["Stage_Name"]
        latest_status = biz_rows.iloc[-1]["Status"]
        completion = compute_completion(biz_id)

        records.append({
            "Business_ID": biz_id,
            "Phase_Current": phase_label,
            "Stage_Current": latest_stage,
            "Status_Current": latest_status,
            "Completion_%": completion,
        })

    phase_summary = pd.DataFrame(records)

    # ✅ Safely build business column list
    biz_cols = ["Business_ID", "Enterprise_Name", "Province",
                "Women_Led", "Youth_Inclusive"]
    if "Window" in business_df.columns:
        biz_cols.insert(1, "Window")

    merged = phase_summary.merge(
        business_df[biz_cols],
        on="Business_ID",
        how="left"
    )

    return merged


def get_businesses_in_phase2(phase_df):
    """
    Returns the set of Business_IDs that have Phase 2 records.
    Useful for debugging or filtering elsewhere.
    """
    return set(
        phase_df[phase_df["Phase"] == "Phase 2"]["Business_ID"].unique()
    )


def show_data_info():
    business_df, phase_df, summary_df = load_data()
    st.subheader("📊 Data Status")
    st.write("Business_DB Rows:", len(business_df))
    st.write("Phase_Tracking Rows:", len(phase_df))
    st.write("Summary Rows:", len(summary_df))
    st.write("Business Columns:", list(business_df.columns))
    st.write("Phase Columns:", list(phase_df.columns))
    st.write("Summary Columns:", list(summary_df.columns))
    st.write("Phase values:", phase_df["Phase"].unique() if not phase_df.empty else "N/A")
    st.write("Phase 2 businesses:", get_businesses_in_phase2(phase_df))