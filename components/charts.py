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

# ✅ Distinct professional colors for provinces
PROVINCE_COLORS = [
    "#2166a8", "#e07b39", "#2a9d8f", "#f4a261", "#1a3a5c",
    "#4a90c4", "#e76f51", "#264653", "#a8dadc", "#e9c46a",
    "#6a4c93", "#c77dff", "#80b918", "#f72585", "#3a86ff",
    "#fb8500", "#8ecae6", "#219ebc", "#023047", "#ffb703",
    "#cb4335", "#1d8348", "#7f8c8d", "#9b59b6", "#2ecc71",
    "#e74c3c", "#3498db", "#f39c12", "#1abc9c", "#d35400",
    "#8e44ad", "#2c3e50", "#16a085", "#c0392b",
]

# ✅ Stage definitions per phase — order matters
PHASE1_STAGES = [
    ("Assessment",       "#2166a8"),   # Primary Blue
    ("Ve-Report",        "#4a90c4"),   # Medium Blue
    ("Selected for BDS", "#2a9d8f"),   # Teal
]

PHASE2_STAGES = [
    ("Dig-Assessment",           "#2166a8"),   # Primary Blue
    ("BP-Development",           "#4a90c4"),   # Medium Blue
    ("Dig-Assessment-Report",    "#2a9d8f"),   # Teal
    ("Virtual E-Capacity-Building",  "#e07b39"),   # Orange
    ("In-Person E-Capacity-Building","#f4a261"),   # Warm Orange
    ("Coaching",                 "#8d6e63"),   # Brownish (new)
    ("Monitoring",               "#1a3a5c"),   # Dark Navy
]

def render_progression_chart(phase_df, phase_label):
    """
    Shows how many businesses are CURRENTLY at each stage.
    Only businesses with "Completed" status count as having reached a stage.
    """

    stages = PHASE1_STAGES if "1" in phase_label else PHASE2_STAGES
    stage_names = [s[0] for s in stages]

    with st.container(border=True):

        st.markdown(f"#### Stage Progression — {phase_label}")

        phase_rows = phase_df[
            phase_df["Phase"].str.strip().str.lower() == phase_label.lower()
        ].copy()

        if phase_rows.empty:
            st.info(f"No stage data available for {phase_label}.")
            return

        phase_rows["Stage_clean"]  = phase_rows["Stage_Name"].str.strip()
        phase_rows["Status_clean"] = phase_rows["Status"].str.strip().str.lower()

        stage_order = {name: i for i, name in enumerate(stage_names)}

        # ✅ Improved logic: only "completed" counts as reaching the stage
        business_current_stage = {}

        for biz_id, group in phase_rows.groupby("Business_ID"):
            best_stage = None
            best_order = -1

            for _, row in group.iterrows():
                stage = row["Stage_clean"]
                status = row["Status_clean"]

                if stage not in stage_order:
                    continue

                if status == "completed":          # ← Only completed counts
                    order = stage_order[stage]
                    if order > best_order:
                        best_order = order
                        best_stage = stage

            if best_stage:
                business_current_stage[biz_id] = best_stage

        if not business_current_stage:
            st.info(f"No active businesses found for {phase_label}.")
            return

        stage_counts = {name: 0 for name in stage_names}
        for biz_id, current_stage in business_current_stage.items():
            if current_stage in stage_counts:
                stage_counts[current_stage] += 1

        total_in_phase = phase_rows["Business_ID"].nunique()

        # Build chart data...
        stage_data = []
        for stage_name, color in stages:
            count = stage_counts.get(stage_name, 0)
            is_final = (stage_name == stage_names[-1])
            all_here = (count == total_in_phase)

            stage_data.append({
                "Stage":        stage_name,
                "Count":        count,
                "Color":        color,
                "AllHere":      all_here,
                "IsFinal":      is_final,
                "Total":        total_in_phase,
            })

        df_stages = pd.DataFrame(stage_data)

        # The rest of the chart code remains the same...
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_stages["Stage"],
            y=df_stages["Count"],
            mode="none",
            fill="tozeroy",
            fillcolor="rgba(33, 102, 168, 0.08)",
            showlegend=False,
            hoverinfo="skip",
        ))

        fig.add_trace(go.Scatter(
            x=df_stages["Stage"],
            y=df_stages["Count"],
            mode="lines",
            line=dict(color="#2166a8", width=2.5),
            showlegend=False,
            hoverinfo="skip",
        ))

        for _, row in df_stages.iterrows():
            count = int(row["Count"])
            all_here = row["AllHere"]
            is_final = row["IsFinal"]

            if is_final and all_here:
                marker_color = "#2a9d8f"
                label = f"✔ {count}"
            elif all_here:
                marker_color = row["Color"]
                label = f"● {count}"
            elif count == 0:
                marker_color = "#cbd5e1"
                label = "0"
            else:
                marker_color = row["Color"]
                label = str(count)

            fig.add_trace(go.Scatter(
                x=[row["Stage"]],
                y=[row["Count"]],
                mode="markers+text",
                marker=dict(size=20, color=marker_color, line=dict(color="white", width=2), symbol="circle"),
                text=[label],
                textposition="top center",
                textfont=dict(size=11, family="Segoe UI", color="#1a3a5c" if count > 0 else "#94a3b8"),
                hovertemplate=f"<b>{row['Stage']}</b><br>Businesses currently here: {count}<br>Out of {int(row['Total'])} total<br><extra></extra>",
                showlegend=False,
            ))

        if total_in_phase > 0:
            fig.add_hline(
                y=total_in_phase,
                line_dash="dot",
                line_color="#cbd5e1",
                line_width=1.5,
                annotation_text=f"Total: {total_in_phase}",
                annotation_position="right",
                annotation_font=dict(size=10, color="#64748b"),
            )

        fig.update_layout(
            height=400,
            margin=dict(t=40, b=80, l=60, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Segoe UI", size=11, color="#475569"),
            xaxis=dict(
                title="Stage",
                titlefont=dict(size=11, color="#64748b"),
                tickfont=dict(size=10),
                categoryorder="array",
                categoryarray=stage_names,
                tickangle=-45,
            ),
            yaxis=dict(
                title="Number of Businesses",
                titlefont=dict(size=11, color="#64748b"),
                gridcolor="#f1f5f9",
                tickfont=dict(size=10),
                range=[0, total_in_phase + 2],
                dtick=1,
            ),
        )

        st.plotly_chart(fig, use_container_width=True, key=f"progression_{phase_label}")
        # ✅ Color legend per stage



def render_charts(filtered_df, phase_df=None, phase_label="Phase 1"):

    st.markdown("#### Visual Analysis")

    # ✅ PROFESSIONAL DONUT — Businesses by Province
    with st.container(border=True):

        province_counts = (
            filtered_df.groupby("Province")["Business_ID"]
            .nunique()
            .reset_index(name="Count")
            .sort_values("Count", ascending=False)
        )

        if province_counts.empty:
            st.info("No province data available.")
        else:
            total = province_counts["Count"].sum()

            # Premium color palette
            colors = [
                "#1e3a8a", "#2563eb", "#3b82f6",
                "#0f766e", "#14b8a6",
                "#b45309", "#f59e0b"
            ][:len(province_counts)]

            fig = go.Figure(go.Pie(
                labels=province_counts["Province"],
                values=province_counts["Count"],
                hole=0.62,  # Larger hole = more modern look
                marker=dict(
                    colors=colors,
                    line=dict(color="white", width=3)
                ),
                textinfo="percent",  # Show only % inside
                textfont=dict(size=13, family="Segoe UI", color="white"),
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Businesses: %{value}<br>"
                    "Share: %{percent}<br>"
                    "<extra></extra>"
                ),
                sort=True,
                direction="clockwise",
            ))

            # Center annotation
            fig.add_annotation(
                text=f"<b>{total}</b><br>Total",
                x=0.5, y=0.5,
                font=dict(size=18, family="Segoe UI", color="#1e293b"),
                showarrow=False,
                align="center"
            )

            fig.update_layout(
                title=dict(
                    text="Businesses by Province",
                    font=dict(size=14, family="Segoe UI", color="#1e293b"),
                    x=0,
                    xanchor="left",
                    y=0.95
                ),
                height=400,
                margin=dict(t=60, b=30, l=20, r=120),  # Space for legend
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Segoe UI", size=11),

                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05,
                    font=dict(size=12, color="#334155"),
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="#e2e8f0",
                    borderwidth=1,
                ),
                showlegend=True,
            )

            st.plotly_chart(
                fig,
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
                    "Not Youth Inclusive":       total - youth_yes,
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
                marker_color="#2166a8",
                text=stacked_df["Women Led"],
                textposition="inside",
                textfont=dict(size=10, color="white"),
            ))

            fig2.add_trace(go.Bar(
                y=stacked_df["Province"],
                x=stacked_df["Not Women Led"],
                name="Not Women Led",
                orientation="h",
                marker_color="#bfdbfe",
                text=stacked_df["Not Women Led"],
                textposition="inside",
                textfont=dict(size=10, color="black"),
            ))

            fig2.add_trace(go.Bar(
                y=stacked_df["Province"],
                x=stacked_df["Youth Inclusive"],
                name="Youth Inclusive",
                orientation="h",
                marker_color="#2a9d8f",
                text=stacked_df["Youth Inclusive"],
                textposition="inside",
                textfont=dict(size=10, color="white"),
                offsetgroup="Youth",
            ))

            fig2.add_trace(go.Bar(
                y=stacked_df["Province"],
                x=stacked_df["Not Youth Inclusive"],
                name="Not Youth Inclusive",
                orientation="h",
                marker_color="#a7f3d0",
                text=stacked_df["Not Youth Inclusive"],
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

def render_businesses_overview(business_df, filtered_df):
    """
    KPI cards + horizontal bar chart for businesses overview.
    """
    # ✅ Filter to only currently filtered businesses
    filtered_biz_ids = filtered_df["Business_ID"].unique()
    filtered_biz = business_df[
        business_df["Business_ID"].isin(filtered_biz_ids)
    ].copy()

    total = len(filtered_biz)


    # ✅ KPI Cards — centered with 2 columns only
    kpi1, kpi2 = st.columns(2)

    with kpi1:
        st.metric("🏢 Total Businesses", total)

    with kpi2:
        province_count = filtered_biz["Province"].dropna().nunique()
        st.metric("📍 Provinces Covered", province_count)

    st.divider()

    # ✅ Bar chart — businesses per province
    if "Province" not in filtered_biz.columns or filtered_biz.empty:
        st.info("No province data available.")
        return

    province_counts = (
        filtered_biz.groupby("Province")["Business_ID"]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=True)
    )

    if province_counts.empty:
        st.info("No province data to display.")
        return

    # ✅ Colors from your palette
    bar_colors = PROVINCE_COLORS[:len(province_counts)]

    fig = go.Figure(go.Bar(
        x=province_counts["Count"],
        y=province_counts["Province"],
        orientation="h",
        marker=dict(
            color=bar_colors,
            line=dict(color="white", width=0.5),
        ),
        text=province_counts["Count"],
        textposition="outside",
        textfont=dict(size=11, family="Segoe UI", color="#1e293b"),
        hovertemplate="<b>%{y}</b><br>Businesses: %{x}<br><extra></extra>",
    ))

    fig.update_layout(
        title=dict(
            text="Businesses in Businesses_DB by Province",
            font=dict(size=14, family="Segoe UI", color="#1e293b"),
            x=0,
        ),
        height=max(220, len(province_counts) * 25 + 60),
        margin=dict(t=50, b=30, l=10, r=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI", size=11),
        xaxis=dict(
            title="Number of Businesses",
            gridcolor="#f1f5f9",
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            title="",
            tickfont=dict(size=11),
            automargin=True,
        ),
    )

    st.plotly_chart(fig, use_container_width=True, key="businesses_by_province_overview")