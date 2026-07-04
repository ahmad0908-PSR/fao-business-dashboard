import streamlit as st

def render_filters(summary_df, business_df):

    st.subheader("🔍 Filters")

    # ✅ Merge Window column from business_df into summary for filtering
    if "Window" not in summary_df.columns and "Business_ID" in business_df.columns:
        window_map = business_df[["Business_ID", "Window"]].drop_duplicates()
        summary_df = summary_df.merge(window_map, on="Business_ID", how="left")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

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

        # ✅ Phase - Custom Display Names
        with col4:
            # Get unique phases from data
            raw_phases = ["All"] + sorted(summary_df["Phase_Current"].dropna().unique().tolist())

            # Map internal values to nice display names
            phase_display_map = {
                "All": "All",
                "Phase 1": "Pre-Qualification Verification",
                "Phase 2": "Business Development Support"
            }

            # Create display options
            phase_options = [phase_display_map.get(p, p) for p in raw_phases]

            # Show nice names to user
            selected_display = st.selectbox("Phase", phase_options)

            # Map back to internal value for filtering
            selected_phase = next((k for k, v in phase_display_map.items() if v == selected_display), selected_display)

    # ✅ Status
    with col5:
        status_options = ["All"] + sorted(summary_df["Status_Current"].dropna().unique().tolist())
        selected_status = st.selectbox("Status", status_options)

    # ✅ Window — NEW
    with col6:
        if "Window" in summary_df.columns:
            window_options = ["All"] + sorted(summary_df["Window"].dropna().unique().tolist())
        else:
            window_options = ["All", "W1A", "W1B", "W2", "W3"]
        selected_window = st.selectbox("Window", window_options)

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

    if selected_window != "All" and "Window" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Window"] == selected_window]

    return filtered_df