import streamlit as st

def render_kpis(filtered_df, business_df):

    st.subheader("📊 Key Performance Indicators")

    # ✅ Total Businesses
    total_business = filtered_df["Business_ID"].nunique()

    # ✅ Women Led %
    women_count = filtered_df[filtered_df["Women_Led"] == "Yes"].shape[0]
    women_percent = (women_count / total_business * 100) if total_business > 0 else 0

    # ✅ Youth %
    youth_count = filtered_df[filtered_df["Youth_Inclusive"] == "Yes"].shape[0]
    youth_percent = (youth_count / total_business * 100) if total_business > 0 else 0

    # ✅ Avg Completion
    avg_completion = filtered_df["Completion_%"].mean()

    # ✅ Financials (from Business_DB)
    merged = filtered_df.merge(business_df, on="Business_ID", how="left")

    total_co = merged["Co_Contribution_USD"].sum()
    total_grant = merged["Grant_Requested_USD"].sum()

    # ✅ Display KPIs
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric("Total Businesses", total_business)
    col2.metric("Women Led %", f"{women_percent:.1f}%")
    col3.metric("Youth Inclusive %", f"{youth_percent:.1f}%")
    col4.metric("Avg Completion %", f"{avg_completion:.1f}%")
    col5.metric("Co-Contribution USD", f"${total_co:,.0f}")
    col6.metric("Total Grant USD", f"${total_grant:,.0f}")