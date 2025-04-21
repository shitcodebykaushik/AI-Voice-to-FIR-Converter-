from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os


def generate_pdf(fir_instance):
    """ Generates a structured FIR PDF similar to Bihar Police format """
    pdf_path = os.path.join("media/fir_pdfs", f"{fir_instance.case_id}.pdf")
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    # Create PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Header
    title = [
        ["FIRST INFORMATION REPORT (FIR)"],
        [f"Case ID: {fir_instance.case_id}"],
        [f"Date & Time: {fir_instance.created_at.strftime('%d/%m/%Y %H:%M')}"]
    ]

    title_table = Table(title, colWidths=[500])
    title_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))

    elements.append(title_table)
    elements.append(Spacer(1, 12))  # Add space

    # Complaint Information
    complaint_details = [
        ["Complainant Details"],
        ["Name", "Unknown"],  # You might need to update this
        ["Address", "Unknown"],
        ["Phone", "Unknown"],
    ]

    complaint_table = Table(complaint_details, colWidths=[150, 350])
    complaint_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ]))

    elements.append(complaint_table)
    elements.append(Spacer(1, 12))

    # Use Paragraphs to Wrap Long Text
    original_text_paragraph = Paragraph(
        fir_instance.original_text, styles["BodyText"])
    fir_text_paragraph = Paragraph(fir_instance.fir_text, styles["BodyText"])

    # FIR Details
    fir_details = [
        ["FIR Details"],
        ["Original Complaint", original_text_paragraph],
        ["Generated FIR", fir_text_paragraph],
    ]

    fir_table = Table(fir_details, colWidths=[150, 350])
    fir_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ]))

    elements.append(fir_table)

    # Build PDF
    doc.build(elements)
    return pdf_path
