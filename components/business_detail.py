import streamlit as st
import pandas as pd
import streamlit.components.v1 as components


def render_business_detail(business_id, business_df, phase_df, summary_df):

    # ✅ Get specific business data
    business = business_df[business_df["Business_ID"] == business_id].iloc[0]
    summary  = summary_df[summary_df["Business_ID"] == business_id].iloc[0]
    phases   = phase_df[phase_df["Business_ID"] == business_id]

    # ✅ BACK BUTTON (top left, native Streamlit)
    if st.button("⬅ Back to Dashboard"):
        st.query_params.clear()
        st.rerun()

    # ✅ PAGE TITLE
    components.html(f"""
    <div style="text-align:center; padding:20px 0 10px 0;">
        <h2 style="color:#2f7aa1; font-family:sans-serif; margin:0;">
            📊 {business.get("Enterprise_Name", "")}
        </h2>
        <p style="color:#888; font-family:sans-serif; margin:4px 0 0 0; font-size:14px;">
            Business ID: {business_id}
        </p>
    </div>
    """, height=100)

    st.divider()

    # ✅ HELPER: render a info card
    def info_card(title, rows):
        items_html = "".join([
            f"""
            <div style="display:flex; justify-content:space-between; padding:6px 0;
                        border-bottom:1px solid #f0f0f0;">
                <span style="color:#555; font-weight:600; font-size:13px;">{k}</span>
                <span style="color:#222; font-size:13px; text-align:right; max-width:60%;">{v}</span>
            </div>
            """
            for k, v in rows
        ])
        return f"""
        <div style="background:#fff; border:1px solid #e0e0e0; border-radius:10px;
                    padding:16px 20px; margin-bottom:16px; box-shadow:0 1px 4px rgba(0,0,0,0.07);">
            <h4 style="color:#2f7aa1; font-family:sans-serif; margin:0 0 10px 0;
                       font-size:15px; border-bottom:2px solid #2f7aa1; padding-bottom:6px;">
                {title}
            </h4>
            {items_html}
        </div>
        """

    # ✅ COMPLETION BADGE COLOR
    completion = summary.get("Completion_%", 0)
    if completion >= 80:
        badge_color = "#5aa07a"
    elif completion >= 50:
        badge_color = "#5b7ea6"
    else:
        badge_color = "#e0a030"

    # ✅ BUILD ALL CARDS
    cards_html = f"""
    <div style="max-width:800px; margin:0 auto; font-family:sans-serif;">

        {info_card("🏢 Business Profile", [
            ("Province",    business.get("Province",   "N/A")),
            ("District",    business.get("District",   "N/A")),
            ("Village",     business.get("Village",    "N/A")),
            ("Owner",       business.get("Owner_Name_Primary", "N/A")),
            ("Window",      business.get("Window",     "N/A")),
            ("Est. Year",   business.get("Year_of_Establishment", "N/A")),
            ("Address",     business.get("Exact_Address", "N/A")),
        ])}

        {info_card("👥 Inclusion & Capacity", [
            ("Women Led",       business.get("Women_Led",             "N/A")),
            ("Youth Inclusive", business.get("Youth_Inclusive",       "N/A")),
            ("Employees",       business.get("Current_Employee_Count","N/A")),
            ("Linked Farmers",  business.get("Current_Linked_Farmers_Count", "N/A")),
        ])}

        {info_card("💰 Financial Information", [
            ("Annual Turnover", f"${int(business.get('Annual_Turnover_USD', 0) or 0):,}"),
            ("Grant Requested", f"${int(business.get('Grant_Requested_USD', 0) or 0):,}"),
            ("Co-Contribution", f"${int(business.get('Co_Contribution_USD',  0) or 0):,}"),
        ])}

        <div style="background:#fff; border:1px solid #e0e0e0; border-radius:10px;
                    padding:16px 20px; margin-bottom:16px; box-shadow:0 1px 4px rgba(0,0,0,0.07);">
            <h4 style="color:#2f7aa1; font-family:sans-serif; margin:0 0 10px 0;
                       font-size:15px; border-bottom:2px solid #2f7aa1; padding-bottom:6px;">
                📈 Progress Overview
            </h4>
            <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #f0f0f0;">
                <span style="color:#555; font-weight:600; font-size:13px;">Current Phase</span>
                <span style="color:#222; font-size:13px;">{summary.get("Phase_Current","N/A")}</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #f0f0f0;">
                <span style="color:#555; font-weight:600; font-size:13px;">Current Stage</span>
                <span style="color:#222; font-size:13px;">{summary.get("Stage_Current","N/A")}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0 4px 0;">
                <span style="color:#555; font-weight:600; font-size:13px;">Completion</span>
                <span style="background:{badge_color}; color:white; border-radius:20px;
                             padding:3px 14px; font-size:13px; font-weight:600;">
                    {completion}%
                </span>
            </div>
            <!-- Progress bar -->
            <div style="background:#e0e0e0; border-radius:10px; height:10px; margin-top:8px;">
                <div style="background:{badge_color}; width:{completion}%; height:10px;
                            border-radius:10px; transition:width 0.4s;"></div>
            </div>
        </div>

    </div>
    """

    components.html(cards_html, height=780, scrolling=True)

    st.divider()

    # ✅ APPLY "SUBMITTED TO FAO" LOGIC — unchanged
    phases_display = phases.copy()

    report_stages = [
        "report development and sumbission 1",
        "report development and submission 2"
    ]

    phases_display.loc[
        (phases_display["Stage_Name"].isin(report_stages)) &
        (phases_display["Status"].str.lower() == "completed"),
        "Status"
    ] = "Submitted to FAO"

    # ✅ PHASE TRACKING TABLE — unchanged
    st.subheader("📋 Phase Tracking Details")

    st.dataframe(
        phases_display[[
            "Phase",
            "Stage_Name",
            "Status",
            "Start_Date",
            "End_Date",
            "Responsible_Officer",
            "Remarks"
        ]],
        use_container_width=True
    )