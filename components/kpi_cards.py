import streamlit as st
import pandas as pd


def count_bds_selection(phase_df, phase_biz_ids):
    """
    Count businesses Selected vs Not Selected for BDS
    by looking at Phase_Tracking rows where:
    - Phase == "Phase 1"
    - Stage_Name == "selected for bds"
    - Status == "Completed" → Selected
    - Status == anything else → Not Selected
    """
    if phase_df is None or phase_df.empty:
        return 0, 0

    # ✅ Filter to Phase 1 "selected for bds" rows only
    bds_rows = phase_df[
        (phase_df["Phase"].str.strip().str.lower() == "phase 1") &
        (phase_df["Stage_Name"].str.strip().str.lower() == "selected for bds") &
        (phase_df["Business_ID"].isin(phase_biz_ids))
    ]

    if bds_rows.empty:
        # ✅ If no "selected for bds" rows exist yet, all are not selected
        return 0, len(phase_biz_ids)

    selected_count = bds_rows[
        bds_rows["Status"].str.strip().str.lower() == "completed"
    ]["Business_ID"].nunique()

    not_selected_count = len(phase_biz_ids) - selected_count

    return selected_count, not_selected_count


def render_kpis(filtered_df, business_df, phase_df, phase_label="Phase 1"):
    """
    Render KPI cards.
    - Phase 1: includes Selected for BDS KPIs
    - Phase 2: includes financial KPIs
    """
    st.markdown("#### Key Performance Indicators")

    phase_biz_ids = filtered_df["Business_ID"].unique()
    total_business = len(phase_biz_ids)

    women_count = filtered_df[filtered_df["Women_Led"] == "Yes"].shape[0]
    women_percent = (women_count / total_business * 100) if total_business > 0 else 0

    youth_count = filtered_df[filtered_df["Youth_Inclusive"] == "Yes"].shape[0]
    youth_percent = (youth_count / total_business * 100) if total_business > 0 else 0

    avg_completion = (
        filtered_df["Completion_%"].mean()
        if "Completion_%" in filtered_df.columns else 0
    )

    # ── PHASE 1 KPIs ──────────────────────────────────────────────────
    if str(phase_label).strip().lower().startswith("phase 1"):

        # ✅ Pass phase_df and the business IDs in this phase
        selected_count, not_selected_count = count_bds_selection(
            phase_df, phase_biz_ids
        )

        col1, col2 = st.columns(2)
        with col1:
            st.metric("🏢 Businesses", total_business)
        with col2:
            st.metric("👩‍💼 Women Led", f"{women_percent:.1f}%")

        col3, col4 = st.columns(2)
        with col3:
            st.metric("👥 Youth Inclusive", f"{youth_percent:.1f}%")
        with col4:
            st.metric("📈 Avg Completion", f"{avg_completion:.1f}%")

        col5, col6 = st.columns(2)
        with col5:
            st.metric("✅ Selected for BDS", selected_count)
        with col6:
            st.metric("❌ Not Selected for BDS", not_selected_count)

    # ── PHASE 2 KPIs ──────────────────────────────────────────────────
    else:
        filtered_business_df = business_df[
            business_df["Business_ID"].isin(phase_biz_ids)
        ]

        # ✅ Safe column access
        total_co = (
            filtered_business_df["Co_Contribution_USD"].sum()
            if "Co_Contribution_USD" in filtered_business_df.columns else 0
        )
        total_grant = (
            filtered_business_df["Grant_Requested_USD"].sum()
            if "Grant_Requested_USD" in filtered_business_df.columns else 0
        )

        col1, col2 = st.columns(2)
        with col1:
            st.metric("🏢 Businesses", total_business)
        with col2:
            st.metric("👩‍💼 Women Led", f"{women_percent:.1f}%")

        col3, col4 = st.columns(2)
        with col3:
            st.metric("👥 Youth Inclusive", f"{youth_percent:.1f}%")
        with col4:
            st.metric("📈 Avg Completion", f"{avg_completion:.1f}%")

        col5, col6 = st.columns(2)
        with col5:
            st.metric("🤝💰 Co-Contribution", f"${total_co:,.0f}")
        with col6:
            st.metric("💵 Grant Total", f"${total_grant:,.0f}")