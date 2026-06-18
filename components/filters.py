import streamlit as st

def render_filters(summary_df):

    st.subheader("🔍 Filters")

    col1, col2, col3, col4, col5 = st.columns(5)

    # ✅ Province
    with col1:
        provinces = ["All"] + sorted(summary_df["Province"].dropna().unique().tolist())
        selected_province = st.selectbox("Province", provinces)

    # ✅ Women Led
    with col2:
        women_options = ["All", "Yes", "No"]
        selected_women = st.selectbox("Women Led", women_options)

    # ✅ Youth Inclusive
    with col3:
        youth_options = ["All", "Yes", "No"]
        selected_youth = st.selectbox("Youth Inclusive", youth_options)

    # ✅ Phase
    with col4:
        phases = ["All"] + sorted(summary_df["Phase_Current"].dropna().unique().tolist())
        selected_phase = st.selectbox("Phase", phases)

    # ✅ Status
    with col5:
        status_options = ["All"] + sorted(summary_df["Status_Current"].dropna().unique().tolist())
        selected_status = st.selectbox("Status", status_options)

    # ✅ APPLY FILTERS
    filtered_df = summary_df.copy()

    if selected_province != "All":
        filtered_df = filtered_df[filtered_df["Province"] == selected_province]

    if selected_women != "All":
        filtered_df = filtered_df[filtered_df["Women_Led"] == selected_women]

    if selected_youth != "All":
        filtered_df = filtered_df[filtered_df["Youth_Inclusive"] == selected_youth]

    if selected_phase != "All":
        filtered_df = filtered_df[filtered_df["Phase_Current"] == selected_phase]

    if selected_status != "All":
        filtered_df = filtered_df[filtered_df["Status_Current"] == selected_status]

    return filtered_df