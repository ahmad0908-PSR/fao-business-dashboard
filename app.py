import streamlit as st
from utils.data_loader import load_data


from components.header import render_header
from components.hero import render_hero
from components.filters import render_filters
from components.kpi_cards import render_kpis
from components.charts import render_charts
from components.table import render_table
from components.footer import render_footer
from components.download import render_downloads



st.set_page_config(page_title="FAO Dashboard", layout="wide")

# ✅ HEADER
render_header()
st.divider()

# ✅ HERO
render_hero()
st.divider()

# ✅ LOAD DATA
business_df, phase_df, summary_df = load_data()

if summary_df is None:
    st.error("❌ Data load failed")
    st.stop()



# ✅ ================================
# ✅ NEW: BUSINESS PROFILE NAVIGATION
# ✅ ================================








# ✅ FILTERS
filtered_df = render_filters(summary_df)
st.divider()

# ✅ KPIs
render_kpis(filtered_df, business_df)
st.divider()

# ✅ Charts
render_charts(filtered_df)
st.divider()


# ✅ Advanced Table (Monitoring Matrix)
render_table(filtered_df, business_df, phase_df)

# ✅ 🔎 View Business Profile (MOVED HERE)
st.subheader("🔎 View Business Profile")

st.markdown("**Select Business**")

col1, col2 = st.columns([3, 1])

# ✅ Dropdown list
business_list = summary_df[["Business_ID", "Enterprise_Name"]].drop_duplicates()

selected_name = col1.selectbox(
    "Select Business",
    business_list["Enterprise_Name"],
    label_visibility="collapsed"
)

# ✅ Get Business ID
selected_business_id = business_list[
    business_list["Enterprise_Name"] == selected_name
]["Business_ID"].values[0]

# ✅ Button click
if col2.button("View Profile 🔍"):
    from components.business_detail import render_business_detail
    render_business_detail(selected_business_id, business_df, phase_df, summary_df)
    st.stop()

st.divider()


# ✅ Downloads
render_downloads(filtered_df, summary_df)

render_footer()
