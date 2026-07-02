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


def get_color(status):
    if pd.isna(status):
        return "#f8fafc"

    status = str(status).lower().strip()

    if "selected" in status or status == "yes":
        return "#fef3c7"

    elif "completed" in status:
        return "#05df72"

    elif "submitted" in status:
        return "#bfdbfe"

    elif "ongoing" in status:
        return "#1e40af"

    elif "not applicable" in status or status in ["n/a", "na"]:
        return "#c7d2fe"

    elif "not started" in status or status == "no":
        return "#e2e8f0"

    else:
        return "#f1f5f9"


def get_text_color(bg_color):
    dark_bg = ["#2166a8", "#1e40af"]
    return "white" if bg_color in dark_bg else "#1e293b"


def render_table(filtered_df, business_df, phase_df):
    st.subheader("📋 FAO-EFSP-BDS Progress")

    # ✅ Strip whitespace from phase data
    phase_df = phase_df.copy()
    phase_df["Stage_Name"] = phase_df["Stage_Name"].str.strip()
    if "Status" in phase_df.columns:
        phase_df["Status"] = phase_df["Status"].str.strip()

    # ✅ Pivot phase data to wide format
    phase_wide = transform_phase_data(phase_df)

    # ✅ Get filtered Business_IDs to respect filters
    filtered_biz_ids = filtered_df["Business_ID"].unique()

    # ✅ Start from business_df filtered to only filtered businesses
    df = business_df[business_df["Business_ID"].isin(filtered_biz_ids)].copy()

    # ✅ Pull app_ID from filtered_df if it exists there but not in business_df
    if "app_ID" not in df.columns and "app_ID" in filtered_df.columns:
        app_id_map = filtered_df[["Business_ID", "app_ID"]].drop_duplicates()
        df = df.merge(app_id_map, on="Business_ID", how="left")

    # ✅ Merge with phase pivot — stage status columns only
    df = df.merge(phase_wide, on="Business_ID", how="left")
    df = df.reset_index(drop=True)

    # ✅ Clean app_ID
    if "app_ID" in df.columns:
        df["app_ID"] = df["app_ID"].fillna("").astype(str).str.strip()
        df["app_ID"] = df["app_ID"].replace("nan", "")

    # ✅ Stage maps
    phase1_stages = {
        "Assessment":       ("Assessment",       "pre"),
        "Ve-Report":        ("Ve-Report",         "pre"),
        "Selected for BDS": ("Selected for BDS",  "pre"),
    }

    phase2_stages = {
        "Dig-Assessment":                  ("Dig-Assessment",                  "bds"),
        "BP-Development":                  ("BP-Development",                   "bds"),
        "Dig-Assessment-Report":           ("Dig-Assessment-Report",            "bds"),
        "Virtual-E-Capacity-Building":     ("Virtual-E-Capacity-Building",      "bds"),
        "In-Person-E-Capacity-Building":   ("In-Person-E-Capacity-Building",    "bds"),
        "Coaching":                        ("Coaching",                         "bds"),
        "Monitoring":                      ("Monitoring",                       "bds"),
    }

    # ✅ Build tbody rows
    tbody_rows = ""
    for i, row in df.iterrows():

        tbody_rows += "<tr>"

        # Row number
        tbody_rows += (
            f"<td style='border:1px solid #ddd; padding:4px 6px; "
            f"text-align:center; color:#1e293b; width:30px;'>{i + 1}</td>"
        )

        # app_ID
        app_id = str(row.get("app_ID", "")).strip()
        if app_id == "nan":
            app_id = ""
        tbody_rows += (
            f"<td style='border:1px solid #ddd; padding:4px 6px; "
            f"text-align:center; color:#1e293b; font-weight:500; width:80px;'>"
            f"{app_id}</td>"
        )

        # Enterprise Name
        tbody_rows += (
            f"<td style='border:1px solid #ddd; padding:4px 6px; "
            f"color:#1e293b; width:150px; word-wrap:break-word;'>"
            f"{row.get('Enterprise_Name', '')}</td>"
        )

        # Province
        tbody_rows += (
            f"<td style='border:1px solid #ddd; padding:4px 6px; "
            f"color:#1e293b; width:70px;'>"
            f"{row.get('Province', '')}</td>"
        )

        # Window
        tbody_rows += (
            f"<td style='border:1px solid #ddd; padding:4px 6px; "
            f"color:#1e293b; width:55px;'>"
            f"{row.get('Window', '')}</td>"
        )

        # Women Led
        tbody_rows += (
            f"<td style='border:1px solid #ddd; padding:4px 6px; "
            f"color:#1e293b; text-align:center; width:60px;'>"
            f"{row.get('Women_Led', '')}</td>"
        )

        # ✅ Phase 1 stages
        for stage_name, (col_name, group) in phase1_stages.items():
            value = row.get(col_name)
            display_value = value

            if stage_name == "Ve-Report":
                if pd.notna(value) and str(value).strip().lower() == "completed":
                    display_value = "Submitted to FAO"

            elif stage_name == "Selected for BDS":
                val_lower = str(value).strip().lower() if pd.notna(value) else ""
                display_value = "Yes" if val_lower == "completed" else "No"

            color = get_color(display_value if pd.notna(display_value) else "")
            text_color = get_text_color(color)
            cell_text = display_value if pd.notna(display_value) else ""
            tbody_rows += (
                f"<td style='border:1px solid #ddd; background-color:{color}; "
                f"color:{text_color}; text-align:center; padding:3px 4px; "
                f"font-size:11px; width:80px; word-wrap:break-word;'>{cell_text}</td>"
            )

        # ✅ Phase 2 stages
        for stage_name, (col_name, group) in phase2_stages.items():
            value = row.get(col_name)
            display_value = value

            if stage_name == "Dig-Assessment-Report":
                if pd.notna(value) and str(value).strip().lower() == "completed":
                    display_value = "Submitted to FAO"

            color = get_color(str(display_value).strip().lower() if pd.notna(display_value) else "")
            text_color = get_text_color(color)
            cell_text = display_value if pd.notna(display_value) else ""
            tbody_rows += (
                f"<td style='border:1px solid #ddd; background-color:{color}; "
                f"color:{text_color}; text-align:center; padding:3px 4px; "
                f"font-size:11px; width:80px; word-wrap:break-word;'>{cell_text}</td>"
            )

        tbody_rows += "</tr>"

    # ✅ Build full HTML - Improved text display
    html = f"""
    <div style="max-height:520px; overflow-y:auto; overflow-x:auto;
                border:1px solid #e2e8f0; border-radius:4px;">
      <table style="border-collapse:collapse; font-size:11.5px; width:100%;">
        <thead>
          <tr>
            <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c;
                color:white; z-index:3; padding:8px 6px; border:1px solid #0f2340;
                width:35px; text-align:center;">#</th>
            <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c;
                color:white; z-index:3; padding:8px 6px; border:1px solid #0f2340;
                width:90px; text-align:center;">App ID</th>
            <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c;
                color:white; z-index:3; padding:8px 6px; border:1px solid #0f2340;
                min-width:180px;">Enterprise Name</th>
            <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c;
                color:white; z-index:3; padding:8px 6px; border:1px solid #0f2340;
                width:80px;">Province</th>
            <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c;
                color:white; z-index:3; padding:8px 6px; border:1px solid #0f2340;
                width:60px;">Window</th>
            <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c;
                color:white; z-index:3; padding:8px 6px; border:1px solid #0f2340;
                width:65px;">Women Led</th>
            <th colspan="3" style="position:sticky; top:0; background-color:#1a3a5c;
                color:white; z-index:3; padding:8px 6px; border:1px solid #0f2340;
                text-align:center;">Pre-Qualification Verification</th>
            <th colspan="7" style="position:sticky; top:0; background-color:#1a3a5c;
                color:white; z-index:3; padding:8px 6px; border:1px solid #0f2340;
                text-align:center;">Business Development Support</th>
          </tr>
          <tr>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px 4px; border:1px solid #1a4f8a;
                font-size:10px; text-align:center; min-width:85px;">Assessment</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px 4px; border:1px solid #1a4f8a;
                font-size:10px; text-align:center; min-width:95px;">Ve-Report</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px 4px; border:1px solid #1a4f8a;
                font-size:10px; text-align:center; min-width:85px;">Selected for BDS</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px 4px; border:1px solid #1a4f8a;
                font-size:10px; text-align:center; min-width:85px;">Dig-Assessment</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px 4px; border:1px solid #1a4f8a;
                font-size:10px; text-align:center; min-width:85px;">BP-Development</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px 4px; border:1px solid #1a4f8a;
                font-size:10px; text-align:center; min-width:110px;">Dig-Assessment-Report</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px 4px; border:1px solid #1a4f8a;
                font-size:10px; text-align:center; min-width:100px;">Virtual E-Capacity</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px 4px; border:1px solid #1a4f8a;
                font-size:10px; text-align:center; min-width:105px;">In-Person E-Capacity</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px 4px; border:1px solid #1a4f8a;
                font-size:10px; text-align:center; min-width:80px;">Coaching</th>
            <th style="position:sticky; top:30px; background-color:#2166a8; color:white;
                z-index:2; padding:6px 4px; border:1px solid #1a4f8a;
                font-size:10px; text-align:center; min-width:85px;">Monitoring</th>
          </tr>
        </thead>
        <tbody>
          {tbody_rows}
        </tbody>
      </table>
    </div>
    """

    components.html(html, height=580, scrolling=True)