import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# ✅ CURRENT TIME
def get_timestamp():
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M"), now.strftime("%Y-%m-%d %H:%M:%S")


# ✅ EXCEL EXPORT
def generate_excel(df):
    from datetime import datetime

    output = BytesIO()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with pd.ExcelWriter(output, engine='openpyxl') as writer:

        # ✅ Add timestamp as a separate sheet
        info_df = pd.DataFrame({
            "Info": ["Generated on"],
            "Value": [now]
        })

        info_df.to_excel(writer, index=False, sheet_name="Info")

        # ✅ Main data
        df.to_excel(writer, index=False, sheet_name="Data")

    return output.getvalue()



# ✅ SIMPLE PDF EXPORT
def generate_pdf(df, title):
    from datetime import datetime
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import landscape, letter
    from reportlab.lib.styles import getSampleStyleSheet

    output = BytesIO()

    # ✅ Landscape page for more width
    doc = SimpleDocTemplate(output, pagesize=landscape(letter))

    styles = getSampleStyleSheet()
    elements = []

    # ✅ Timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ✅ Title + Timestamp
    elements.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f"Generated on: {now}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # ✅ Convert dataframe to list
    data = [list(df.columns)]

    for _, row in df.iterrows():
        row_data = []
        for val in row:
            text = str(val)

            # ✅ Prevent extremely long text
            if len(text) > 30:
                text = text[:30] + "..."

            row_data.append(text)

        data.append(row_data)

    # ✅ Create table
    table = Table(data, repeatRows=1)

    # ✅ Styling
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2f7aa1")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),

        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 6),  # ✅ Small to fit all columns

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    elements.append(table)

    # ✅ Build PDF
    doc.build(elements)

    output.seek(0)
    return output


# ✅ DOWNLOAD BUTTONS
def render_downloads(filtered_df, raw_df):

    st.subheader("⬇️ Download Data")

    ts_file, ts_text = get_timestamp()

    col1, col2, col3, col4 = st.columns(4)

    # ✅ FILTERED EXCEL
    col1.download_button(
        label="Download Filtered Excel",
        data=generate_excel(filtered_df),
        file_name=f"Filtered_Data_{ts_file}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # ✅ RAW EXCEL
    col2.download_button(
        label="Download Raw Excel",
        data=generate_excel(raw_df),
        file_name=f"Raw_Data_{ts_file}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # ✅ FILTERED PDF
    col3.download_button(
        label="Download Filtered PDF",
        data=generate_pdf(filtered_df, "Filtered Business Data"),
        file_name=f"Filtered_Data_{ts_file}.pdf",
        mime="application/pdf"
    )

    # ✅ RAW PDF
    col4.download_button(
        label="Download Raw PDF",
        data=generate_pdf(raw_df, "Raw Business Data"),
        file_name=f"Raw_Data_{ts_file}.pdf",
        mime="application/pdf"
    )

    st.caption(f"Generated on: {ts_text}")