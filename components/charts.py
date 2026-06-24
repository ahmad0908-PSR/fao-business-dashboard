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
                [0.0, "#7ec8e3"],
                [0.5, "#2166a8"],
                [1.0, "#1a3a5c"],
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

        # ✅ STACKED BAR — Women Led vs Youth Inclusive by Province
        with st.container(border=True):
            if "Province" not in filtered_df.columns:
                st.info("Province data not available.")
            else:
                # ✅ Build counts per province for each inclusion metric
                provinces = filtered_df["Province"].dropna().unique()

                records = []
                for province in provinces:
                    prov_df = filtered_df[filtered_df["Province"] == province]
                    total = len(prov_df)

                    women_yes = prov_df[prov_df["Women_Led"] == "Yes"].shape[0]
                    women_no = total - women_yes

                    youth_yes = prov_df[prov_df["Youth_Inclusive"] == "Yes"].shape[0]
                    youth_no = total - youth_yes

                    records.append({
                        "Province": province,
                        "Women Led": women_yes,
                        "Not Women Led": women_no,
                        "Youth Inclusive": youth_yes,
                        "Not Youth": youth_no,
                        "Total": total,
                    })

                stacked_df = pd.DataFrame(records).sort_values("Total", ascending=True)

                # ✅ Melt into long format for grouped stacked bar
                women_df = stacked_df[["Province", "Women Led", "Not Women Led"]].copy()
                women_df = women_df.melt(
                    id_vars="Province",
                    value_vars=["Women Led", "Not Women Led"],
                    var_name="Category",
                    value_name="Count",
                )
                women_df["Group"] = "Women Led"

                youth_df = stacked_df[["Province", "Youth Inclusive", "Not Youth"]].copy()
                youth_df = youth_df.melt(
                    id_vars="Province",
                    value_vars=["Youth Inclusive", "Not Youth"],
                    var_name="Category",
                    value_name="Count",
                )
                youth_df["Group"] = "Youth Inclusive"

                # ✅ Build figure with two trace groups
                fig3 = go.Figure()

                color_map = {
                    "Women Led": "#2a9d8f",
                    "Not Women Led": "#cbd5e1",
                    "Youth Inclusive": "#2166a8",
                    "Not Youth": "#e2e8f0",
                }

                for category, color in color_map.items():
                    if category in ["Women Led", "Not Women Led"]:
                        source_df = women_df[women_df["Category"] == category]
                    else:
                        source_df = youth_df[youth_df["Category"] == category]

                    fig3.add_trace(go.Bar(
                        name=category,
                        y=source_df["Province"],
                        x=source_df["Count"],
                        orientation="h",
                        marker=dict(color=color, line=dict(width=0)),
                        text=source_df["Count"].apply(lambda v: str(int(v)) if v > 0 else ""),
                        textposition="inside",
                        textfont=dict(size=10, color="white", family="Segoe UI"),
                        hovertemplate=(
                            "<b>%{y}</b><br>"
                            f"{category}: %{{x}}<br>"
                            "<extra></extra>"
                        ),
                        offsetgroup=category.split()[0],
                    ))

                fig3.update_layout(
                    title=dict(
                        text="Women Led & Youth Inclusive by Province",
                        font=dict(size=13, family="Segoe UI", color="#1e293b"),
                        x=0,
                        xanchor="left",
                    ),
                    barmode="stack",
                    height=380,
                    margin=dict(t=50, b=80, l=10, r=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Segoe UI", size=11, color="#475569"),
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.2,
                        xanchor="center",
                        x=0,
                        font=dict(size=10),
                    ),
                    xaxis=dict(title="", gridcolor="#f1f5f9", tickfont=dict(size=10)),
                    yaxis=dict(title="", tickfont=dict(size=10)),
                    bargap=0.2,
                    bargroupgap=0.1,
                )

                # ✅ Only render ONCE with unique key
                st.plotly_chart(
                    fig3,
                    use_container_width=True,
                    key=f"stacked_{phase_label}"
                )