import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def render_charts(filtered_df, phase_df=None, phase_label="Phase 1"):

    st.markdown("#### Visual Analysis")

    # ✅ STATUS DONUT
    with st.container(border=True):
        status_counts = filtered_df["Status_Current"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]

        fig1 = px.pie(
            status_counts,
            names="Status",
            values="Count",
            hole=0.5,
            title="Business Status Distribution",
            color_discrete_sequence=[
                "#2166a8", "#e07b39", "#2a9d8f",
                "#4a90c4", "#f4a261",
            ],
        )
        fig1.update_layout(
            height=320,
            margin=dict(t=40, b=20, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Segoe UI", size=11),
            title=dict(font=dict(size=13, color="#1e293b")),
            legend=dict(font=dict(size=10)),
        )
        fig1.update_traces(
            textfont=dict(size=11, family="Segoe UI"),
        )
        st.plotly_chart(                                    # ✅ unique key added
            fig1,
            use_container_width=True,
            key=f"donut_{phase_label}"
        )

    # ✅ HORIZONTAL BAR — Businesses by Province
    with st.container(border=True):
        province_counts = filtered_df["Province"].value_counts().reset_index()
        province_counts.columns = ["Province", "Count"]
        province_counts = province_counts.sort_values(by="Count", ascending=True)

        fig2 = px.bar(
            province_counts,
            x="Count",
            y="Province",
            orientation="h",
            title="Businesses by Province",
            color="Count",
            color_continuous_scale=[
                [0.0, "#e59057"],
                [0.5, "#e59057"],
                [1.0, "#e59057"],
            ],
        )
        fig2.update_layout(
            height=320,
            margin=dict(t=40, b=20, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Segoe UI", size=11),
            title=dict(font=dict(size=13, color="#1e293b")),
            coloraxis_showscale=False,
            xaxis=dict(
                title="",
                gridcolor="#f1f5f9",
                tickfont=dict(size=10),
            ),
            yaxis=dict(
                title="",
                tickfont=dict(size=10),
            ),
        )
        fig2.update_traces(
            texttemplate="%{x}",
            textposition="outside",
            textfont=dict(size=10),
        )
        st.plotly_chart(                                    # ✅ unique key added
            fig2,
            use_container_width=True,
            key=f"bar_{phase_label}"
        )

        # ✅ STACKED BAR — Women Led & Youth Inclusive by Province
        with st.container(border=True):
            if "Province" not in filtered_df.columns:
                st.info("Province data not available.")
            else:
                provinces = filtered_df["Province"].dropna().unique()

                records = []
                for province in provinces:
                    prov_df = filtered_df[filtered_df["Province"] == province]
                    total = len(prov_df)

                    women_yes = prov_df[prov_df["Women_Led"] == "Yes"].shape[0]
                    youth_yes = prov_df[prov_df["Youth_Inclusive"] == "Yes"].shape[0]

                    records.append({
                        "Province": province,
                        "Women Led": women_yes,
                        "Not Women Led": total - women_yes,
                        "Youth Inclusive": youth_yes,
                        "Not Youth": total - youth_yes,
                    })

                stacked_df = pd.DataFrame(records).sort_values(
                    by=["Women Led", "Youth Inclusive"], ascending=True
                )

                # Create the figure
                fig3 = go.Figure()

                # Women Led stack (bottom)
                fig3.add_trace(go.Bar(
                    y=stacked_df["Province"],
                    x=stacked_df["Women Led"],
                    name="Women Led",
                    orientation="h",
                    marker_color="#2f7aa1",          # Dark blue
                    text=stacked_df["Women Led"],
                    textposition="inside",
                    textfont=dict(size=10, color="white"),
                ))

                fig3.add_trace(go.Bar(
                    y=stacked_df["Province"],
                    x=stacked_df["Not Women Led"],
                    name="Not Women Led",
                    orientation="h",
                    marker_color="#cbd5e1",          # Light gray
                    text=stacked_df["Not Women Led"],
                    textposition="inside",
                    textfont=dict(size=10, color="black"),
                ))

                # Youth Inclusive stack (bottom)
                fig3.add_trace(go.Bar(
                    y=stacked_df["Province"],
                    x=stacked_df["Youth Inclusive"],
                    name="Youth Inclusive",
                    orientation="h",
                    marker_color="#4a9fc7",          # Medium blue/teal
                    text=stacked_df["Youth Inclusive"],
                    textposition="inside",
                    textfont=dict(size=10, color="white"),
                    offsetgroup="Youth",             # Separate group
                ))

                fig3.add_trace(go.Bar(
                    y=stacked_df["Province"],
                    x=stacked_df["Not Youth"],
                    name="Not Youth",
                    orientation="h",
                    marker_color="#e2e8f0",          # Very light gray
                    text=stacked_df["Not Youth"],
                    textposition="inside",
                    textfont=dict(size=10, color="black"),
                    offsetgroup="Youth",
                ))

                fig3.update_layout(
                    title="Women Led & Youth Inclusive by Province",
                    barmode="stack",
                    height=420,
                    margin=dict(t=50, b=80, l=10, r=20),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Segoe UI", size=11),
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.25,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=10)
                    ),
                    xaxis=dict(title="", gridcolor="#f1f5f9", tickfont=dict(size=10)),
                    yaxis=dict(title="", tickfont=dict(size=10), automargin=True),
                    bargap=0.25,
                    bargroupgap=0.15,
                )

                st.plotly_chart(
                    fig3,
                    use_container_width=True,
                    key=f"stacked_{phase_label}"
                )