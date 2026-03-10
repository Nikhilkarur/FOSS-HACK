from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def generate_scan_report_pdf(user_id: int, scan_data: list) -> bytes:
    """
    Generate a PDF report of a user's scan history.

    :param user_id:   The ID of the user.
    :param scan_data: List of dicts, each with keys:
                        product_name, health_score, verdict, created_at,
                        ingredients (list of {name, flags}).
    :return: Raw PDF bytes.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=11,
        spaceAfter=6,
        textColor=colors.grey,
    )
    section_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=13,
        spaceAfter=8,
        spaceBefore=14,
    )
    warning_style = ParagraphStyle(
        "AllergyWarning",
        parent=styles["Normal"],
        textColor=colors.HexColor("#b71c1c"),
        fontSize=10,
        spaceAfter=4,
    )

    story = []

    # ── Header ──────────────────────────────────────────────────────────────
    story.append(Paragraph("NutriScan Report", title_style))
    story.append(Paragraph(f"User ID: {user_id}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 0.2 * inch))

    if not scan_data:
        story.append(Paragraph("No scan history found.", styles["Normal"]))
        doc.build(story)
        return buffer.getvalue()

    # ── Scan History Table ───────────────────────────────────────────────────
    story.append(Paragraph("Recent Scans", section_style))

    header = ["#", "Product Name", "Health Score", "Verdict", "Date"]
    rows = [header]
    allergy_warnings: list[str] = []

    for i, scan in enumerate(scan_data, start=1):
        product = scan.get("product_name") or "Unknown"
        score = scan.get("health_score", "N/A")
        verdict = scan.get("verdict", "N/A")
        created_at = scan.get("created_at")
        date_str = (
            created_at.strftime("%Y-%m-%d %H:%M")
            if hasattr(created_at, "strftime")
            else str(created_at)
        )
        score_str = f"{score:.1f}" if isinstance(score, float) else str(score)
        rows.append([str(i), product, score_str, verdict, date_str])

        # Collect allergen-flagged ingredients
        for ing in scan.get("ingredients", []):
            flags = (ing.get("flags") or "").lower()
            if "allergen" in flags:
                allergy_warnings.append(
                    f"Scan #{i} \u2014 {product}: "
                    f"{ing.get('name', 'Unknown')} ({ing.get('flags', '')})"
                )

    col_widths = [0.35 * inch, 2.5 * inch, 1.1 * inch, 1.4 * inch, 1.5 * inch]
    table = Table(rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                # Header row
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2e7d32")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                # Body rows
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#f1f8e9")],
                ),
                # All cells
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 0.3 * inch))

    # ── Allergy Warnings ─────────────────────────────────────────────────────
    story.append(Paragraph("Allergy Warnings", section_style))
    if allergy_warnings:
        for warning in allergy_warnings:
            story.append(Paragraph(f"\u26a0 {warning}", warning_style))
    else:
        story.append(
            Paragraph(
                "No allergy warnings found in your recent scans.", styles["Normal"]
            )
        )

    doc.build(story)
    return buffer.getvalue()
