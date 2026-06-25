import streamlit as st
import pandas as pd
import streamlit.components.v1 as components


def transform_phase_data(phase_df):
    """Pivot Phase_Tracking to wide format using exact Stage_Name values."""
    pivot = phase_df.pivot_table(
        index="Business_ID",
        columns="Stage_Name",
        values="Status",
        aggfunc="first"
    ).reset_index()
    return pivot


def transform_capacity_type(phase_df):
    """
    Extract Capacity_Building_Type per Business_ID
    for the E-Capacity-Building stage.
    """
    if "Capacity_Building_Type" not in phase_df.columns:
        return {}

    cap_rows = phase_df[
        phase_df["Stage_Name"].str.strip() == "E-Capacity-Building"
    ][["Business_ID", "Capacity_Building_Type"]].drop_duplicates("Business_ID")

    return dict(zip(cap_rows["Business_ID"], cap_rows["Capacity_Building_Type"]))


def get_color(status):
    if pd.isna(status):
        return "#f8fafc"

    status = str(status).lower().strip()

    if "selected" in status or status == "yes":
        return "#fef3c7"                # ✅ Amber — Selected / Yes

    elif "completed" in status:
        return "#d1fae5"                # ✅ Soft green — Completed

    elif "submitted" in status:
        return "#dbeafe"                # ✅ Light blue — Submitted to FAO

    elif "ongoing" in status:
        return "#2166a8"                # ✅ Primary blue — Ongoing

    elif "not started" in status or status == "no":
        return "#f1f5f9"                # ✅ Light grey — Not Started / No

    else:
        return "#ffffff"


def get_text_color(bg_color):
    """Return white text for dark backgrounds, dark for light ones."""
    dark_bg = ["#2166a8"]
    return "white" if bg_color in dark_bg else "#1e293b"


def render_table(filtered_df, business_df, phase_df):

    st.subheader("📋 FAO-EFSP-BDS Progress")

    # ✅ Strip Stage_Name whitespace to avoid matching issues
    phase_df = phase_df.copy()
    phase_df["Stage_Name"] = phase_df["Stage_Name"].str.strip()
    if "Status" in phase_df.columns:
        phase_df["Status"] = phase_df["Status"].str.strip()

    # ✅ Pivot phase data to wide format
    phase_wide = transform_phase_data(phase_df)

    # ✅ Get capacity building type per business
    capacity_type_map = transform_capacity_type(phase_df)

    # ✅ Merge summary with pivot
    df = filtered_df.copy()
    df = df.merge(phase_wide, on="Business_ID", how="left")
    df = df.reset_index(drop=True)

    # ✅ Stage map — keys match EXACT Stage_Name values in your sheet now
    # Phase 1 stages
    phase1_stages = {
        "Assessment":       ("Assessment",      "pre"),
        "Ve-Report":        ("Ve-Report",        "pre"),
        "Selected for BDS": ("Selected for BDS", "pre"),
    }

    # Phase 2 stages
    phase2_stages = {
        "Dig-Assessment":        ("Dig-Assessment",        "bds"),
        "BP-Development":        ("BP-Development",         "bds"),
        "Dig-Assessment-Report": ("Dig-Assessment-Report",  "bds"),
        "E-Capacity-Building":   ("E-Capacity-Building",    "bds"),
        "Coaching":              ("Coaching",               "bds"),
        "Monitoring":            ("Monitoring",             "bds"),
    }

    # ✅ Build tbody rows
    tbody_rows = ""
    for i, row in df.iterrows():
        biz_id = row.get("Business_ID", "")
        cap_type = capacity_type_map.get(biz_id, "")

        tbody_rows += "<tr>"
        tbody_rows += f"<td style='border:1px solid #ddd; padding:6px; text-align:center; color:#1e293b;'>{i + 1}</td>"
        tbody_rows += f"<td style='border:1px solid #ddd; padding:6px; min-width:160px; color:#1e293b;'>{row.get('Enterprise_Name', '')}</td>"
        tbody_rows += f"<td style='border:1px solid #ddd; padding:6px; color:#1e293b;'>{row.get('Province', '')}</td>"
        tbody_rows += f"<td style='border:1px solid #ddd; padding:6px; color:#1e293b;'>{row.get('Window', '')}</td>"
        tbody_rows += f"<td style='border:1px solid #ddd; padding:6px; color:#1e293b;'>{row.get('Women_Led', '')}</td>"

        # ✅ Phase 1 stages
        for stage_name, (col_name, group) in phase1_stages.items():
            value = row.get(col_name)
            display_value = value

            # Ve-Report: Completed → Submitted to FAO
            if stage_name == "Ve-Report":
                if pd.notna(value) and str(value).strip().lower() == "completed":
                    display_value = "Submitted to FAO"

            # Selected for BDS: Completed → Yes, Not Started → No
            elif stage_name == "Selected for BDS":
                val_lower = str(value).strip().lower() if pd.notna(value) else ""
                if val_lower == "completed":
                    display_value = "Yes"
                elif val_lower in ["not started", "nan", ""]:
                    display_value = "No"

            color = get_color(display_value if pd.notna(display_value) else "")
            text_color = get_text_color(color)
            cell_text = display_value if pd.notna(display_value) else ""
            tbody_rows += (
                f"<td style='border:1px solid #ddd; background-color:{color}; "
                f"color:{text_color}; text-align:center; padding:4px; "
                f"white-space:nowrap;'>{cell_text}</td>"
            )

        # ✅ Phase 2 stages
        for stage_name, (col_name, group) in phase2_stages.items():
            value = row.get(col_name)
            display_value = value

            # Dig-Assessment-Report: Completed → Submitted to FAO
            if stage_name == "Dig-Assessment-Report":
                if pd.notna(value) and str(value).strip().lower() == "completed":
                    display_value = "Submitted to FAO"

            # E-Capacity-Building: show Type in brackets if available
            elif stage_name == "E-Capacity-Building":
                if pd.notna(value) and str(value).strip().lower() != "":
                    if cap_type and str(cap_type).strip() not in ["", "nan"]:
                        display_value = f"{value} ({cap_type})"
                    else:
                        display_value = value

            color = get_color(str(display_value).strip().lower() if pd.notna(display_value) else "")
            text_color = get_text_color(color)
            cell_text = display_value if pd.notna(display_value) else ""
            tbody_rows += (
                f"<td style='border:1px solid #ddd; background-color:{color}; "
                f"color:{text_color}; text-align:center; padding:4px; "
                f"white-space:nowrap;'>{cell_text}</td>"
            )

        tbody_rows += "</tr>"

    # ✅ Build full HTML — OUTSIDE the for loop (critical fix)
    html = f"""
    <div style="max-height:500px; overflow-y:auto; overflow-x:auto; border:1px solid #e2e8f0;">
      <table style="width:100%; border-collapse:collapse; font-size:12px;">
        <thead>
          <tr>
            <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c;
                color:white; z-index:3; padding:8px; border:1px solid #0f2340;">#</th>
            <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c;
                color:white; z-index:3; padding:8px; border:1px solid #0f2340;">Enterprise Name</th>
            <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c;
                color:white; z-index:3; padding:8px; border:1px solid #0f2340;">Province</th>
            <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c;
                color:white; z-index:3; padding:8px; border:1px solid #0f2340;">Window</th>
            <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c;
                color:white; z-index:3; padding:8px; border:1px solid #0f2340;">Women Led</th>
            <th colspan="3" style="position:sticky; top:0; background-color:#1a3a5c;
                color:white; z-index:3; padding:8px; border:1px solid #0f2340;
                text-align:center;">Pre-Qualification Verification</th>
            <th colspan="6" style="position:sticky; top:0; background-color:#1a3a5c;
                color:white; z-index:3; padding:8px; border:1px solid #0f2340;
                text-align:center;">Business Development Support</th>
          </tr>
          <tr>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px; border:1px solid #1a4f8a;">Assessment</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px; border:1px solid #1a4f8a;">Ve-Report</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px; border:1px solid #1a4f8a;">Selected for BDS</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px; border:1px solid #1a4f8a;">Dig-Assessment</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px; border:1px solid #1a4f8a;">BP-Development</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px; border:1px solid #1a4f8a;">Dig-Assessment-Report</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px; border:1px solid #1a4f8a;">E-Capacity-Building</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px; border:1px solid #1a4f8a;">Coaching</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px; border:1px solid #1a4f8a;">Monitoring</th>
          </tr>
        </thead>
        <tbody>
          {tbody_rows}
        </tbody>
      </table>
    </div>
    """

    components.html(html, height=550, scrolling=True)