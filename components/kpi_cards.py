import streamlit as st
import pandas as pd


def count_bds_selection(phase_df, phase_biz_ids):
    """
    Count businesses for Selected for BDS stage.

    Status mapping:
    - completed          → Selected
    - ongoing            → Pending/FAO
    - not selected/fao   → Not Selected
    - all other statuses or missing records → ignored
    """

    if phase_df is None or phase_df.empty or len(phase_biz_ids) == 0:
        return 0, 0, 0

    # Filter Phase 1 → Selected for BDS
    bds_rows = phase_df[
        (phase_df["Phase"].str.strip().str.lower() == "phase 1") &
        (phase_df["Stage_Name"].str.strip().str.lower() == "selected for bds") &
        (phase_df["Business_ID"].isin(phase_biz_ids))
    ]

    if bds_rows.empty:
        return 0, 0, 0

    status_series = bds_rows["Status"].fillna("").str.strip().str.lower()

    selected_count = bds_rows[
        status_series == "completed"
    ]["Business_ID"].nunique()

    pending_count = bds_rows[
        status_series == "ongoing"
    ]["Business_ID"].nunique()

    not_selected_count = bds_rows[
        status_series == "not selected/fao"
    ]["Business_ID"].nunique()

    return selected_count, pending_count, not_selected_count

def render_kpis(filtered_df, business_df, phase_df, phase_label="Phase 1"):
    """
    Render KPI cards.
    - Phase 1: includes Selected for BDS KPIs
    - Phase 2: includes financial KPIs
    """
    st.markdown("#### Key Performance Indicators")

    phase_biz_ids = filtered_df["Business_ID"].unique() if filtered_df is not None else []
    total_business = len(phase_biz_ids)

    women_count = filtered_df[filtered_df["Women_Led"] == "Yes"].shape[0] if filtered_df is not None else 0
    women_percent = (women_count / total_business * 100) if total_business > 0 else 0

    youth_count = filtered_df[filtered_df["Youth_Inclusive"] == "Yes"].shape[0] if filtered_df is not None else 0
    youth_percent = (youth_count / total_business * 100) if total_business > 0 else 0

    # ── PHASE 1 KPIs ──────────────────────────────────────────────────
    if str(phase_label).strip().lower().startswith("phase 1"):

        # Avg Completion (only Assessment + Ve-Report)
        phase1_stages_for_completion = ["Assessment", "Ve-Report"]

        if phase_df is not None and not phase_df.empty:
            p1_rows = phase_df[
                (phase_df["Phase"].str.strip() == "Phase 1") &
                (phase_df["Stage_Name"].str.strip().isin(phase1_stages_for_completion)) &
                (phase_df["Business_ID"].isin(phase_biz_ids))
            ]

            if not p1_rows.empty:
                completion_per_biz = []
                for biz_id in phase_biz_ids:
                    biz_rows = p1_rows[p1_rows["Business_ID"] == biz_id]
                    completed = biz_rows[
                        biz_rows["Status"].str.strip().str.lower() == "completed"
                    ].shape[0]
                    completion_per_biz.append((completed / 2) * 100)
                avg_completion = sum(completion_per_biz) / len(completion_per_biz) if completion_per_biz else 0
            else:
                avg_completion = 0
        else:
            avg_completion = 0

        # Get the three counts
        selected_count, pending_count, not_selected_count = count_bds_selection(
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

        # New layout with 3 cards for BDS status
        col5, col6, col7 = st.columns(3)
        with col5:
            st.metric("✅ Selected  BDS", selected_count)
        with col6:
            st.metric("⏳ Pending/FAO", pending_count)
        with col7:
            st.metric("❌ Not Selected  BDS", not_selected_count)

    # ── PHASE 2 KPIs ──────────────────────────────────────────────────
    else:
        avg_completion = (
            filtered_df["Completion_%"].mean()
            if filtered_df is not None and "Completion_%" in filtered_df.columns else 0
        )

        filtered_business_df = business_df[
            business_df["Business_ID"].isin(phase_biz_ids)
        ] if business_df is not None else pd.DataFrame()

        total_co = filtered_business_df.get("Co_Contribution_USD", pd.Series(0)).sum()
        total_grant = filtered_business_df.get("Grant_Requested_USD", pd.Series(0)).sum()

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