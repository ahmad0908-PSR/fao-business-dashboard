import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# ✅ Accurate province centroids for all 34 Afghanistan provinces
PROVINCE_CENTROIDS = {
    "Badakhshan":  (70.8,  37.1),
    "Badghis":     (63.7,  35.2),
    "Baghlan":     (68.7,  36.1),
    "Balkh":       (67.0,  36.8),
    "Bamyan":      (67.8,  34.8),
    "Daikundi":    (66.4,  33.7),
    "Farah":       (62.4,  32.4),
    "Faryab":      (64.9,  36.1),
    "Ghazni":      (68.4,  33.5),
    "Ghor":        (64.9,  34.1),
    "Helmand":     (64.2,  31.3),
    "Herat":       (62.2,  34.4),
    "Jawzjan":     (66.4,  36.9),
    "Kabul":       (69.2,  34.5),
    "Kandahar":    (65.7,  31.6),
    "Kapisa":      (69.6,  34.9),
    "Khost":       (69.9,  33.3),
    "Kunar":       (71.1,  34.8),
    "Kunduz":      (68.9,  36.7),
    "Laghman":     (70.1,  34.7),
    "Logar":       (69.1,  34.0),
    "Nangarhar":   (70.6,  34.2),
    "Nimroz":      (62.0,  30.9),
    "Nuristan":    (70.7,  35.4),
    "Paktia":      (69.4,  33.7),
    "Paktika":     (69.3,  32.3),
    "Panjshir":    (69.6,  35.6),
    "Parwan":      (68.8,  35.1),
    "Samangan":    (67.9,  36.2),
    "Sar-e Pol":   (65.9,  36.2),
    "Takhar":      (69.5,  36.7),
    "Uruzgan":     (66.6,  32.9),
    "Wardak":      (68.2,  34.1),
    "Zabul":       (67.2,  32.1),
}


def render_map(filtered_df):

    st.markdown("### Geographic Distribution")
    st.caption("Total businesses per province — filtered view")

    # ✅ Count businesses per province
    province_counts = (
        filtered_df.groupby("Province")["Business_ID"]
        .nunique()
        .reset_index()
    )
    province_counts.columns = ["Province", "Total Businesses"]

    if province_counts.empty:
        st.info("No province data to display.")
        return

    # ✅ Add lat/lon from centroids
    province_counts["lon"] = province_counts["Province"].map(
        lambda x: PROVINCE_CENTROIDS.get(x, (None, None))[0]
    )
    province_counts["lat"] = province_counts["Province"].map(
        lambda x: PROVINCE_CENTROIDS.get(x, (None, None))[1]
    )

    # ✅ Drop any provinces without coordinates
    province_counts = province_counts.dropna(subset=["lat", "lon"])

    if province_counts.empty:
        st.warning("Province names in your data don't match the map. "
                   f"Found: {filtered_df['Province'].unique().tolist()}")
        return

    # ✅ Build bubble map
    fig = go.Figure()

    # Background: all provinces as faint grey dots
    all_provinces = pd.DataFrame([
        {"Province": p, "lon": v[0], "lat": v[1]}
        for p, v in PROVINCE_CENTROIDS.items()
    ])

    fig.add_trace(go.Scattergeo(
        lon=all_provinces["lon"],
        lat=all_provinces["lat"],
        text=all_provinces["Province"],
        mode="markers+text",
        marker=dict(
            size=6,
            color="#cbd5e1",
            line=dict(width=0),
        ),
        textfont=dict(size=7, color="#94a3b8"),
        textposition="top center",
        hoverinfo="text",
        name="All Provinces",
        showlegend=False,
    ))

    # Active provinces: colored bubbles sized by business count
    fig.add_trace(go.Scattergeo(
        lon=province_counts["lon"],
        lat=province_counts["lat"],
        text=province_counts["Province"],
        customdata=province_counts["Total Businesses"],
        mode="markers+text",
        marker=dict(
            size=province_counts["Total Businesses"] * 14 + 16,
            color=province_counts["Total Businesses"],
            colorscale=[
                [0.0, "#7ec8e3"],
                [0.5, "#2166a8"],
                [1.0, "#1a3a5c"],
            ],
            showscale=True,
            colorbar=dict(
                title="Businesses",
                thickness=12,
                len=0.5,
                tickfont=dict(size=10, family="Segoe UI"),
                titlefont=dict(size=11, family="Segoe UI"),
            ),
            line=dict(width=1.5, color="white"),
            opacity=0.85,
        ),
        textfont=dict(size=8, color="#1e293b", family="Segoe UI"),
        textposition="top center",
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Businesses: %{customdata}<br>"
            "<extra></extra>"
        ),
        name="Active Provinces",
        showlegend=False,
    ))

    fig.update_geos(
        scope="asia",
        center=dict(lon=67.5, lat=33.9),
        projection_scale=5.5,
        showland=True,
        landcolor="#f8fafc",
        showocean=True,
        oceancolor="#e8f4f8",
        showlakes=False,
        showrivers=False,
        showcountries=True,
        countrycolor="#cbd5e1",
        countrywidth=1,
        showframe=False,
        bgcolor="rgba(0,0,0,0)",
    )

    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI", size=11),
        geo=dict(bgcolor="rgba(0,0,0,0)"),
    )

    st.plotly_chart(fig, use_container_width=True)

    # ✅ Province breakdown table
    with st.expander("View Province Breakdown", expanded=False):
        display_df = province_counts[["Province", "Total Businesses"]].sort_values(
            "Total Businesses", ascending=False
        ).reset_index(drop=True)
        display_df.index += 1
        st.dataframe(display_df, use_container_width=True)