import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# ✅ Distinct professional colors for provinces
PROVINCE_COLORS = [
    "#2166a8",  # Primary Blue
    "#e07b39",  # Orange
    "#2a9d8f",  # Teal
    "#f4a261",  # Warm Orange
    "#1a3a5c",  # Dark Navy
    "#4a90c4",  # Medium Blue
    "#e76f51",  # Coral
    "#264653",  # Dark Teal
    "#a8dadc",  # Light Teal
    "#e9c46a",  # Yellow
    "#6a4c93",  # Purple
    "#c77dff",  # Light Purple
    "#80b918",  # Green
    "#f72585",  # Pink
    "#3a86ff",  # Bright Blue
    "#fb8500",  # Amber
    "#8ecae6",  # Sky Blue
    "#219ebc",  # Ocean Blue
    "#023047",  # Deep Navy
    "#ffb703",  # Gold
    "#cb4335",  # Red
    "#1d8348",  # Forest Green
    "#7f8c8d",  # Grey
    "#9b59b6",  # Violet
    "#2ecc71",  # Emerald
    "#e74c3c",  # Crimson
    "#3498db",  # Dodger Blue
    "#f39c12",  # Sunflower
    "#1abc9c",  # Turquoise
    "#d35400",  # Pumpkin
    "#8e44ad",  # Wisteria
    "#2c3e50",  # Wet Asphalt
    "#16a085",  # Green Sea
    "#c0392b",  # Pomegranate
]


def render_charts(filtered_df, phase_df=None, phase_label="Phase 1"):

    st.markdown("#### Visual Analysis")

    # ✅ DONUT — Businesses by Province (replaces old status donut + bar chart)
    with st.container(border=True):

        province_counts = (
            filtered_df.groupby("Province")["Business_ID"]
            .nunique()
            .reset_index()
        )
        province_counts.columns = ["Province", "Count"]
        province_counts = province_counts.sort_values(
            "Count", ascending=False
        ).reset_index(drop=True)

        if province_counts.empty:
            st.info("No province data available.")
        else:
            # ✅ Assign a distinct color to each province
            colors = PROVINCE_COLORS[:len(province_counts)]

            fig1 = go.Figure(go.Pie(
                labels=province_counts["Province"],
                values=province_counts["Count"],
                hole=0.5,
                marker=dict(
                    colors=colors,
                    line=dict(color="white", width=2),
                ),
                textinfo="label+percent",
                textfont=dict(size=11, family="Segoe UI"),
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Businesses: %{value}<br>"
                    "Share: %{percent}<br>"
                    "<extra></extra>"
                ),
                direction="clockwise",
                sort=True,
            ))

            fig1.update_layout(
                title=dict(
                    text="Businesses by Province",
                    font=dict(size=13, family="Segoe UI", color="#1e293b"),
                    x=0,
                    xanchor="left",
                ),
                height=380,
                margin=dict(t=50, b=20, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Segoe UI", size=11),
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    font=dict(size=10),
                ),
                annotations=[
                    dict(
                        text=f"<b>{province_counts['Count'].sum()}</b><br>Total",
                        x=0.5, y=0.5,
                        font=dict(
                            size=14,
                            family="Segoe UI",
                            color="#1a3a5c",
                        ),
                        showarrow=False,
                    )
                ],
            )

            st.plotly_chart(
                fig1,
                use_container_width=True,
                key=f"province_donut_{phase_label}"
            )

    # ✅ STACKED BAR — Women Led & Youth Inclusive by Province (unchanged)
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
                    "Province":        province,
                    "Women Led":       women_yes,
                    "Not Women Led":   total - women_yes,
                    "Youth Inclusive": youth_yes,
                    "Not Youth":       total - youth_yes,
                })

            stacked_df = pd.DataFrame(records).sort_values(
                by=["Women Led", "Youth Inclusive"], ascending=True
            )

            fig2 = go.Figure()

            fig2.add_trace(go.Bar(
                y=stacked_df["Province"],
                x=stacked_df["Women Led"],
                name="Women Led",
                orientation="h",
                marker_color="#2f7aa1",
                text=stacked_df["Women Led"],
                textposition="inside",
                textfont=dict(size=10, color="white"),
            ))

            fig2.add_trace(go.Bar(
                y=stacked_df["Province"],
                x=stacked_df["Not Women Led"],
                name="Not Women Led",
                orientation="h",
                marker_color="#cbd5e1",
                text=stacked_df["Not Women Led"],
                textposition="inside",
                textfont=dict(size=10, color="black"),
            ))

            fig2.add_trace(go.Bar(
                y=stacked_df["Province"],
                x=stacked_df["Youth Inclusive"],
                name="Youth Inclusive",
                orientation="h",
                marker_color="#4a9fc7",
                text=stacked_df["Youth Inclusive"],
                textposition="inside",
                textfont=dict(size=10, color="white"),
                offsetgroup="Youth",
            ))

            fig2.add_trace(go.Bar(
                y=stacked_df["Province"],
                x=stacked_df["Not Youth"],
                name="Not Youth",
                orientation="h",
                marker_color="#e2e8f0",
                text=stacked_df["Not Youth"],
                textposition="inside",
                textfont=dict(size=10, color="black"),
                offsetgroup="Youth",
            ))

            fig2.update_layout(
                title=dict(
                    text="Women Led & Youth Inclusive by Province",
                    font=dict(size=13, family="Segoe UI", color="#1e293b"),
                    x=0,
                    xanchor="left",
                ),
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
                    font=dict(size=10),
                ),
                xaxis=dict(
                    title="",
                    gridcolor="#f1f5f9",
                    tickfont=dict(size=10),
                ),
                yaxis=dict(
                    title="",
                    tickfont=dict(size=10),
                    automargin=True,
                ),
                bargap=0.25,
                bargroupgap=0.15,
            )

            st.plotly_chart(
                fig2,
                use_container_width=True,
                key=f"stacked_{phase_label}"
            )