import streamlit as st
from utils.data_loader import load_data, build_phase_summary

from components.header import render_header
from components.filters import render_filters
from components.kpi_cards import render_kpis
from components.charts import render_charts, render_progression_chart, render_businesses_overview  # ✅ single clean import
from components.map import render_map
from components.table import render_table
from components.footer import render_footer
from components.download import render_downloads


st.set_page_config(page_title="FAO Dashboard", layout="wide")

st.markdown("""
<style>

/* ── Global font ── */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* ── Page background ── */
[data-testid="stAppViewContainer"] {
    background-color: #f1f5f9;
}

/* ── Bordered Containers ───────────────────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #dbe4ee !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    padding: 14px !important;
    margin-bottom: 12px !important;
}

/* Remove borders from nested containers */
[data-testid="stVerticalBlockBorderWrapper"]
[data-testid="stVerticalBlockBorderWrapper"] {
    border: none !important;
    border-top: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
    background: transparent !important;
}

/* ── KPI metric cards ── */
[data-testid="stMetric"] {
    background-color: #2369A4 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 6px !important;
    padding: 10px 12px !important;
    box-shadow: none !important;
}

/* ── KPI label ── */
[data-testid="stMetricLabel"] > div {
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    color: #ffffff !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: unset !important;
}

/* ── KPI value ── */
[data-testid="stMetricValue"] > div {
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: unset !important;
}

/* ── Phase titles (h3) ── */
[data-testid="stMarkdownContainer"] h3 {
    font-size: 13px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: #1e293b !important;
    margin-bottom: 2px !important;
    border-left: 4px solid #e07b39;
    padding-left: 10px;
}

/* ── Section subheaders (h4) ── */
[data-testid="stMarkdownContainer"] h4 {
    font-size: 10px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: #94a3b8 !important;
    margin-top: 14px !important;
    margin-bottom: 8px !important;
}

/* ── Caption ── */
[data-testid="stCaptionContainer"] p {
    color: #94a3b8 !important;
    font-size: 11px !important;
    margin-top: 0 !important;
}

/* ── Divider ── */
hr {
    border-color: #e2e8f0 !important;
    margin: 10px 0 !important;
}

/* ── Buttons ── */
[data-testid="stButton"] button {
    background-color: transparent !important;
    border: 1px solid #2166a8 !important;
    color: #2166a8 !important;
    font-size: 11px !important;
    padding: 4px 10px !important;
    border-radius: 4px !important;
    white-space: nowrap !important;
    transition: all 0.2s ease !important;
}

[data-testid="stButton"] button:hover {
    background-color: #2166a8 !important;
    border-color: #2166a8 !important;
    color: #ffffff !important;
}

/* ── Radio ── */
[data-testid="stRadio"] label {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #475569 !important;
}

/* ── Filters section background ── */
[data-testid="stSelectbox"] > div > div {
    background-color: #2369A4 !important;   /* ← change dropdown bg */
    border-color: #e2e8f0 !important;
}

/* ── Selectbox selected value text color ── */
[data-testid="stSelectbox"] div[data-baseweb="select"] div {
    color: #ffffff !important;              /* ← text color when closed */
}

/* ── Selectbox dropdown options text ── */
[data-testid="stSelectbox"] ul li {
    color: #1e293b !important;              /* ← text color in open dropdown */
}
</style>
""", unsafe_allow_html=True)

# ✅ HEADER
render_header()
st.divider()

# ✅ LOAD DATA
business_df, phase_df, summary_df = load_data()

if summary_df is None or summary_df.empty:
    st.error("❌ Data load failed")
    st.stop()

# ✅ Refresh button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# ✅ FILTERS
filtered_df = render_filters(summary_df, business_df)
st.divider()

# ✅ BUSINESSES OVERVIEW — KPI + bar chart (below filters, above FAO chart)
st.markdown("### FAO Assigned Businesses")
st.caption("Total businesses Assigned by FAO")
with st.container(border=True):
    render_businesses_overview(business_df, filtered_df)
st.divider()

# ✅ MAP
with st.container(border=True):
    render_map(filtered_df)
st.divider()

# ✅ GET FILTERED BUSINESS IDs
filtered_biz_ids = filtered_df["Business_ID"].unique()
filtered_phase_df = phase_df[phase_df["Business_ID"].isin(filtered_biz_ids)]

# ✅ BUILD PHASE-SPECIFIC SUMMARIES
phase1_df = build_phase_summary(filtered_phase_df, business_df, summary_df, "Phase 1")
phase2_df = build_phase_summary(filtered_phase_df, business_df, summary_df, "Phase 2")

# ✅ KPI + CHART SECTION
phase_col1, phase_col2 = st.columns(2)

# ── PHASE 1 ──
with phase_col1:
    with st.container(border=True):
        st.markdown("### Phase 1 — Pre-Qualification")
        st.caption("Assessment & verification stages")
        st.divider()
        if phase1_df.empty:
            st.info("No Phase 1 data available.")
        else:
            render_kpis(phase1_df, business_df, phase_df, phase_label="Phase 1")
            render_progression_chart(filtered_phase_df, "Phase 1")   # ✅ NOW CALLED
            render_charts(phase1_df, phase_df=filtered_phase_df, phase_label="Phase 1")

# ── PHASE 2 ──
with phase_col2:
    with st.container(border=True):
        st.markdown("### Phase 2 — Business Development Support")
        st.caption("Capacity building & grant utilization stages")
        st.divider()
        if phase2_df.empty:
            st.info("No Phase 2 data available.")
        else:
            render_kpis(phase2_df, business_df, phase_df, phase_label="Phase 2")
            render_progression_chart(filtered_phase_df, "Phase 2")   # ✅ NOW CALLED
            render_charts(phase2_df, phase_df=filtered_phase_df, phase_label="Phase 2")

st.divider()

# ✅ TABLE
render_table(filtered_df, business_df, phase_df)

st.divider()

# ✅ BUSINESS PROFILE
st.markdown("### Business Profile Lookup")
st.caption("Search and view detailed profile for any business")

# ✅ Build business list from summary_df
business_list = summary_df[["Business_ID", "Enterprise_Name"]].drop_duplicates().reset_index(drop=True)

# ✅ Add app_ID if available in summary_df or business_df
if "app_ID" in summary_df.columns:
    business_list = summary_df[["Business_ID", "Enterprise_Name", "app_ID"]].drop_duplicates().reset_index(drop=True)
elif "app_ID" in business_df.columns:
    app_id_map = business_df[["Business_ID", "app_ID"]].drop_duplicates()
    business_list = business_list.merge(app_id_map, on="Business_ID", how="left")

# ✅ Clean up app_ID
if "app_ID" in business_list.columns:
    business_list["app_ID"] = business_list["app_ID"].fillna("").astype(str).str.strip().replace("nan", "")

profile_col1, profile_col2 = st.columns([3, 1])

with profile_col1:
    search_query = st.text_input(
        "Search business",
        placeholder="Type any part of name or App ID...",
        label_visibility="collapsed"
    )

    query = search_query.strip().lower()

    if query:
        # ✅ Search in Enterprise_Name
        name_mask = business_list["Enterprise_Name"].str.lower().str.contains(
            query, na=False, regex=False      # regex=False avoids special char issues
        )

        # ✅ Search in app_ID if available
        if "app_ID" in business_list.columns:
            id_mask = business_list["app_ID"].str.lower().str.contains(
                query, na=False, regex=False
            )
            # ✅ Search in Business_ID as well
            biz_id_mask = business_list["Business_ID"].str.lower().str.contains(
                query, na=False, regex=False
            )
            combined_mask = name_mask | id_mask | biz_id_mask
        else:
            biz_id_mask = business_list["Business_ID"].str.lower().str.contains(
                query, na=False, regex=False
            )
            combined_mask = name_mask | biz_id_mask

        filtered_list = business_list[combined_mask].reset_index(drop=True)
    else:
        filtered_list = business_list

    if filtered_list.empty:
        st.warning(f"No business found matching '{search_query}' — try a shorter keyword")
        selected_name = None
    else:
        selected_name = st.selectbox(
            "Select Business",
            filtered_list["Enterprise_Name"],
            label_visibility="collapsed"
        )

with profile_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    view_clicked = st.button("View Profile →")

if selected_name and view_clicked:
    selected_business_id = business_list[
        business_list["Enterprise_Name"] == selected_name
    ]["Business_ID"].values[0]
    from components.business_detail import render_business_detail
    render_business_detail(selected_business_id, business_df, phase_df, summary_df)
    st.stop()

st.divider()

# ✅ DOWNLOADS
render_downloads(filtered_df, summary_df)

render_footer()