import streamlit as st
import pandas as pd
import streamlit.components.v1 as components


def transform_phase_data(phase_df):
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

    if "selected" in status:
        return "#fef3c7"

    elif status == "yes" or "completed" in status:
        return "#d1fae5"  # Strong green - for Completed and Yes

    elif "submitted" in status:
        return "#dbeafe"  # Light green - for Submitted to FAO

    elif "ongoing" in status:
        return "#2166a8"  # Blue - for Ongoing

    elif status == "no" or "not started" in status:
        return "#f1f5f9"  # Gray - for Not Started and No

    else:
        return "#ffffff"


def render_table(filtered_df, business_df, phase_df):

    st.subheader("📋 FAO-EFSP-BDS Progress")

    # Transform phase data to wide format
    phase_wide = transform_phase_data(phase_df)

    # Merge filtered summary with phase pivot
    df = filtered_df.copy()
    df = df.merge(phase_wide, on="Business_ID", how="left")
    df = df.reset_index(drop=True)

    # Stage column mapping (key = display label, value = actual column name after pivot)
    stage_map = {
        "assessment":           "assessment",
        "ver_report":           "report development and sumbission 1",
        "selected_bds":         "selected for bds", # I added this new choice in the spreadsheets!
        "diagnostic":           "diagnostic assessment and capacity building",
        "bp_dev":               "business plan development",
        "report2":              "report development and submission 2",
        "capacity":             "one-day capacity-building orientation covering five modules and grant utilization",
        "coaching":             "follow-up, monitoring, and documentation of success stories"
    }

    # ── Build tbody rows ──────────────────────────────────────────────
    tbody_rows = ""
    for i, row in df.iterrows():                          # ✅ df, not merged_df
        tbody_rows += "<tr>"
        tbody_rows += f"<td style='border:1px solid #ddd; padding:6px; text-align:center;'>{i + 1}</td>"
        tbody_rows += f"<td style='border:1px solid #ddd; padding:6px; min-width:160px;'>{row.get('Enterprise_Name', '')}</td>"
        tbody_rows += f"<td style='border:1px solid #ddd; padding:6px;'>{row.get('Province', '')}</td>"
        tbody_rows += f"<td style='border:1px solid #ddd; padding:6px;'>{row.get('Window', '')}</td>"
        tbody_rows += f"<td style='border:1px solid #ddd; padding:6px;'>{row.get('Women_Led', '')}</td>"

        for key, col_name in stage_map.items():
            value = row.get(col_name)
            display_value = value

            # Report stages: show "Submitted to FAO" instead of "Completed"
            if key in ["ver_report", "report2"]:
                if str(value).lower() == "completed":
                    display_value = "Submitted to FAO"

            # 2. NEW: Selected for BDS stage: "Completed" → "Yes"
            elif key == "selected_bds":
                if str(value).lower() == "completed":
                    display_value = "Yes"
                elif str(value).lower() in ["not started", "nan", ""]:
                    display_value = "No"  # Optional: show "No" instead of blank
                # else: keep original status (e.g. "Ongoing")

            color = get_color(display_value)
            cell_text = display_value if pd.notna(display_value) else ""
            tbody_rows += (
                f"<td style='border:1px solid #ddd; background-color:{color}; "
                f"text-align:center; padding:4px; white-space:nowrap;'>{cell_text}</td>"
            )

        tbody_rows += "</tr>"

        # ── Build full HTML (once) ────────────────────────────────────────
        html = f"""
        <div style="max-height:500px; overflow-y:auto; overflow-x:auto; border:1px solid #444;">
          <table style="width:100%; border-collapse:collapse; font-size:12px;">
            <thead>
              <tr>
                <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c; color:white; z-index:3; padding:8px; border:1px solid #1a5f7a;">#</th>
                <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c; color:white; z-index:3; padding:8px; border:1px solid #1a5f7a;">Enterprise Name</th>
                <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c; color:white; z-index:3; padding:8px; border:1px solid #1a5f7a;">Province</th>
                <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c; color:white; z-index:3; padding:8px; border:1px solid #1a5f7a;">Window</th>
                <th rowspan="2" style="position:sticky; top:0; background-color:#1a3a5c; color:white; z-index:3; padding:8px; border:1px solid #1a5f7a;">Women Led</th>
                <th colspan="3" style="position:sticky; top:0; background-color:#1a3a5c; color:white; z-index:3; padding:8px; border:1px solid #1a5f7a; text-align:center;">Pre-Qualification Verification</th>
                <th colspan="5" style="position:sticky; top:0; background-color:#1a3a5c; color:white; z-index:3; padding:8px; border:1px solid #1a5f7a; text-align:center;">Business Development Support</th>
              </tr>
              <tr>
                <th style="position:sticky; top:30px; background-color:#2166a8; color:white; z-index:2; padding:6px; border:1px solid #2f7aa1;">Assessment</th>
                <th style="position:sticky; top:30px; background-color:#2166a8; color:white; z-index:2; padding:6px; border:1px solid #2f7aa1;">Ve-Report</th>
                <th style="position:sticky; top:30px; background-color:#2166a8; color:white; z-index:2; padding:6px; border:1px solid #2f7aa1;">Selected for BDS</th>
                <th style="position:sticky; top:30px; background-color:#2166a8; color:white; z-index:2; padding:6px; border:1px solid #2f7aa1;">Dig-Assessment</th>
                <th style="position:sticky; top:30px; background-color:#2166a8; color:white; z-index:2; padding:6px; border:1px solid #2f7aa1;">BP-Development</th>
                <th style="position:sticky; top:30px; background-color:#2166a8; color:white; z-index:2; padding:6px; border:1px solid #2f7aa1;">Dig-Assessment-Report</th>
                <th style="position:sticky; top:30px; background-color:#2166a8; color:white; z-index:2; padding:6px; border:1px solid #2f7aa1;">E-Capacity Building</th>
                <th style="position:sticky; top:30px; background-color:#2166a8; color:white; z-index:2; padding:6px; border:1px solid #2f7aa1;">Coaching/Monitoring</th>
              </tr>
            </thead>
            <tbody>
              {tbody_rows}
            </tbody>
          </table>
        </div>
        """

    # ✅ Single render call — components.html for sticky headers to work
    components.html(html, height=550, scrolling=True)