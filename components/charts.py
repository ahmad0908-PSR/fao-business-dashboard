import streamlit as st
import plotly.express as px


def render_charts(filtered_df):

    st.subheader("📊 Visual Analysis")

    col1, col2, col3 = st.columns(3)

    # ✅ 1. STATUS DONUT
    with col1:
        status_counts = filtered_df["Status_Current"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]

        fig1 = px.pie(
            status_counts,
            names="Status",
            values="Count",
            title="Status Breakdown",
            hole=0.5
        )

        st.plotly_chart(fig1, use_container_width=True)

    # ✅ 2. PROVINCE BAR CHART
    with col2:
        province_counts = filtered_df["Province"].value_counts().reset_index()
        province_counts.columns = ["Province", "Count"]

        fig2 = px.bar(
            province_counts,
            x="Province",
            y="Count",
            title="Businesses per Province"
        )

        fig2.update_layout(xaxis_tickangle=-45)

        st.plotly_chart(fig2, use_container_width=True)

    # ✅ 3. PHASE BAR CHART
    with col3:
        phase_counts = filtered_df["Phase_Current"].value_counts().reset_index()
        phase_counts.columns = ["Phase", "Count"]

        fig3 = px.bar(
            phase_counts,
            x="Phase",
            y="Count",
            title="Businesses per Phase"
        )

        st.plotly_chart(fig3, use_container_width=True)