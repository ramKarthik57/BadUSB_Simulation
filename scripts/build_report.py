import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import win32com.client
import pymupdf as fitz  # PyMuPDF
from PIL import Image, ImageDraw

REPORTS_DIR = os.path.abspath("reports")
ASSETS_DIR = os.path.join(REPORTS_DIR, "assets")
REVIEW_DIR = os.path.join(REPORTS_DIR, "visual_review")
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(REVIEW_DIR, exist_ok=True)

DOCX_PATH = os.path.join(REPORTS_DIR, "ESP32_S3_HID_Project_Report.docx")
PDF_PATH = os.path.join(REPORTS_DIR, "ESP32_S3_HID_Project_Report.pdf")

# Color Palette Constants
HEX_NAVY_PRIMARY = "14263D"
HEX_NAVY_SECONDARY = "243B53"
HEX_TEAL_ACCENT = "0F9D92"
HEX_BLUE_TECH = "3273B9"
HEX_BG_LIGHT = "F1F5F9"
HEX_BG_ZEBRA = "F8FAFC"
HEX_BORDER = "D7E0E8"

RGB_NAVY_PRIMARY = RGBColor(0x14, 0x26, 0x3D)
RGB_NAVY_SECONDARY = RGBColor(0x24, 0x3B, 0x53)
RGB_TEAL_ACCENT = RGBColor(0x0F, 0x9D, 0x92)
RGB_BLUE_TECH = RGBColor(0x32, 0x73, 0xB9)
RGB_TEXT_MAIN = RGBColor(0x27, 0x34, 0x44)
RGB_TEXT_MUTED = RGBColor(0x64, 0x74, 0x8B)
RGB_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RGB_GREEN_PASS = RGBColor(0x15, 0x80, 0x3D)


def set_cell_background(cell, hex_color):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_margins(cell, top=50, bottom=50, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_borders(table, border_color=HEX_BORDER):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="{HEX_NAVY_PRIMARY}"/>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f"</w:tblBorders>"
    )
    tblPr.append(borders)


def prevent_row_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:cantSplit"))


def repeat_header_row(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:tblHeader"))


def add_bottom_border_to_paragraph(paragraph, color_hex=HEX_TEAL_ACCENT, sz="10"):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="2" w:color="{color_hex}"/>'
        f"</w:pBdr>"
    )
    pPr.append(pBdr)


def add_field(paragraph, field_name):
    run = paragraph.add_run()
    run.font.name = "Segoe UI"
    run.font.size = Pt(8.0)
    run.font.color.rgb = RGB_TEXT_MUTED
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls("w"))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> %s </w:instrText>' % (nsdecls("w"), field_name))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls("w"))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls("w"))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def setup_headers_and_footers(doc):
    section = doc.sections[0]
    section.different_first_page_header_footer = True

    # Running Header (Pages 2..8) - Fits cleanly on 1 line
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.paragraph_format.space_before = Pt(0)
    hp.paragraph_format.space_after = Pt(2)
    hrun1 = hp.add_run("ESP32-S3 Phone-Controlled USB HID & BadUSB Defense Platform  |  ")
    hrun1.font.name = "Segoe UI"
    hrun1.font.size = Pt(8.0)
    hrun1.font.bold = True
    hrun1.font.color.rgb = RGB_NAVY_PRIMARY
    hrun2 = hp.add_run("Department of Cybersecurity, Amrita Vishwa Vidyapeetham")
    hrun2.font.name = "Segoe UI"
    hrun2.font.size = Pt(8.0)
    hrun2.font.color.rgb = RGB_TEXT_MUTED
    add_bottom_border_to_paragraph(hp, HEX_BORDER, "6")

    # Running Footer (Pages 2..8)
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fp.paragraph_format.space_before = Pt(2)
    fp.paragraph_format.space_after = Pt(0)
    frun1 = fp.add_run("Ram Karthik G & Harini V (CH.SC.U4CYS23037 & CH.SC.U4CYS23010)          Page ")
    frun1.font.name = "Segoe UI"
    frun1.font.size = Pt(8.0)
    frun1.font.color.rgb = RGB_TEXT_MUTED
    add_field(fp, "PAGE")
    frun2 = fp.add_run(" of ")
    frun2.font.name = "Segoe UI"
    frun2.font.size = Pt(8.0)
    frun2.font.color.rgb = RGB_TEXT_MUTED
    add_field(fp, "NUMPAGES")

    # First Page Footer
    fp_first = section.first_page_footer.paragraphs[0]
    fp_first.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp_first.paragraph_format.space_before = Pt(2)
    fp_first.paragraph_format.space_after = Pt(0)
    fp_first_run = fp_first.add_run(
        "Technical Project Report  •  Department of Cybersecurity, Amrita Vishwa Vidyapeetham, Chennai  •  Page 1 of 8"
    )
    fp_first_run.font.name = "Segoe UI"
    fp_first_run.font.size = Pt(8.0)
    fp_first_run.font.color.rgb = RGB_TEXT_MUTED


def add_section_h1(doc, num_str, title_str, space_before=0, space_after=3):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True

    r_num = p.add_run(f"SECTION {num_str}  |  ")
    r_num.font.name = "Segoe UI"
    r_num.font.size = Pt(12.5)
    r_num.font.bold = True
    r_num.font.color.rgb = RGB_TEAL_ACCENT

    r_title = p.add_run(title_str.upper())
    r_title.font.name = "Segoe UI"
    r_title.font.size = Pt(12.5)
    r_title.font.bold = True
    r_title.font.color.rgb = RGB_NAVY_PRIMARY

    add_bottom_border_to_paragraph(p, HEX_TEAL_ACCENT, "10")
    return p


def add_section_h2(doc, sub_str, space_before=4, space_after=1.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(sub_str)
    r.font.name = "Segoe UI"
    r.font.size = Pt(10.2)
    r.font.bold = True
    r.font.color.rgb = RGB_NAVY_SECONDARY
    return p


def add_formatted_runs(p, text, base_size=9.0, base_color=RGB_TEXT_MAIN):
    parts = text.split("`")
    for idx, part in enumerate(parts):
        if not part:
            continue
        r = p.add_run(part)
        if idx % 2 == 1:
            # Inline code span
            r.font.name = "Consolas"
            r.font.size = Pt(base_size - 0.5)
            r.font.bold = True
            r.font.color.rgb = RGB_NAVY_SECONDARY
        else:
            r.font.name = "Segoe UI"
            r.font.size = Pt(base_size)
            r.font.color.rgb = base_color


def add_body_p(doc, text, bold_prefix=None, space_after=2.5, line_spacing=1.07, font_size=9.0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = "Segoe UI"
        rb.font.size = Pt(font_size)
        rb.font.bold = True
        rb.font.color.rgb = RGB_NAVY_PRIMARY
    add_formatted_runs(p, text, base_size=font_size, base_color=RGB_TEXT_MAIN)
    return p


def add_bullet_p(doc, bold_lead, text, space_after=2.0, font_size=8.9):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Mm(4.0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.06

    r_dot = p.add_run("▪  ")
    r_dot.font.name = "Segoe UI"
    r_dot.font.size = Pt(font_size)
    r_dot.font.bold = True
    r_dot.font.color.rgb = RGB_TEAL_ACCENT

    r_lead = p.add_run(bold_lead)
    r_lead.font.name = "Segoe UI"
    r_lead.font.size = Pt(font_size)
    r_lead.font.bold = True
    r_lead.font.color.rgb = RGB_NAVY_PRIMARY

    add_formatted_runs(p, text, base_size=font_size, base_color=RGB_TEXT_MAIN)
    return p


def add_callout_box(doc, title, text, accent_hex=HEX_TEAL_ACCENT, bg_hex=HEX_BG_LIGHT):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Mm(178)
    cell = tbl.cell(0, 0)
    cell.width = Mm(178)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=65, bottom=65, left=140, right=120)
    prevent_row_split(tbl.rows[0])

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{accent_hex}"/>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>'
        f"</w:tcBorders>"
    )
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.06

    rt = p.add_run(title + "  ")
    rt.font.name = "Segoe UI"
    rt.font.size = Pt(8.8)
    rt.font.bold = True
    rt.font.color.rgb = RGB_NAVY_PRIMARY

    add_formatted_runs(p, text, base_size=8.8, base_color=RGB_TEXT_MAIN)


def add_figure_block(doc, img_filename, caption_text, width_mm=170, space_before=2, space_after=2.5):
    img_path = os.path.join(ASSETS_DIR, img_filename)
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(space_before)
    p_img.paragraph_format.space_after = Pt(1.5)
    p_img.paragraph_format.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Mm(width_mm))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(space_after)
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = "Segoe UI"
    r_cap.font.size = Pt(8.0)
    r_cap.font.italic = True
    r_cap.font.color.rgb = RGB_TEXT_MUTED


def add_styled_table(doc, headers, rows_data, col_widths_mm, caption_text=None, font_size=8.0, cell_pad_v=36, space_before=2):
    if caption_text:
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(space_before)
        p_cap.paragraph_format.space_after = Pt(1.5)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = "Segoe UI"
        r_cap.font.size = Pt(8.3)
        r_cap.font.bold = True
        r_cap.font.color.rgb = RGB_NAVY_PRIMARY

    tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl)

    # Header Row
    hdr_row = tbl.rows[0]
    repeat_header_row(hdr_row)
    prevent_row_split(hdr_row)
    for c_idx, h_text in enumerate(headers):
        cell = hdr_row.cells[c_idx]
        cell.width = Mm(col_widths_mm[c_idx])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_background(cell, HEX_NAVY_PRIMARY)
        set_cell_margins(cell, top=cell_pad_v + 10, bottom=cell_pad_v + 10, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == len(headers) - 1 and len(h_text) <= 8 else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        r.font.name = "Segoe UI"
        r.font.size = Pt(font_size)
        r.font.bold = True
        r.font.color.rgb = RGB_WHITE

    # Data Rows
    for r_idx, row_vals in enumerate(rows_data):
        row = tbl.rows[r_idx + 1]
        prevent_row_split(row)
        bg = HEX_BG_ZEBRA if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.width = Mm(col_widths_mm[c_idx])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=cell_pad_v, bottom=cell_pad_v, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.03

            is_status_col = val in ("PASS", "1", "2", "3", "4")
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if is_status_col else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Consolas" if (c_idx == 1 and "test_" in val) else "Segoe UI"
            r.font.size = Pt(font_size - 0.3 if "test_" in val else font_size)
            if val == "PASS":
                r.font.bold = True
                r.font.color.rgb = RGB_GREEN_PASS
            elif c_idx == 0:
                r.font.bold = True
                r.font.color.rgb = RGB_NAVY_PRIMARY
            else:
                r.font.color.rgb = RGB_TEXT_MAIN


def build_docx():
    doc = Document()

    # Prevent Microsoft Word from downsampling or compressing 4K embedded images
    settings_el = doc.settings.element
    if settings_el.find(qn("w:doNotCompressPictures")) is None:
        settings_el.append(OxmlElement("w:doNotCompressPictures"))

    # Configure A4 Portrait Page Setup (210mm x 297mm) with 12mm top/bottom and 16mm left/right margins
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(12)
    section.bottom_margin = Mm(12)
    section.left_margin = Mm(16)
    section.right_margin = Mm(16)
    section.header_distance = Mm(5.5)
    section.footer_distance = Mm(5.5)

    setup_headers_and_footers(doc)

    # =========================================================================
    # PAGE 1: TITLE PAGE, METADATA PANEL, EXECUTIVE SUMMARY & CAPABILITY MATRIX
    # =========================================================================
    banner_tbl = doc.add_table(rows=1, cols=1)
    banner_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    banner_tbl.autofit = False
    banner_tbl.columns[0].width = Mm(178)
    bcell = banner_tbl.cell(0, 0)
    bcell.width = Mm(178)
    set_cell_background(bcell, HEX_NAVY_PRIMARY)
    set_cell_margins(bcell, top=110, bottom=110, left=150, right=150)

    bp1 = bcell.paragraphs[0]
    bp1.paragraph_format.space_before = Pt(0)
    bp1.paragraph_format.space_after = Pt(2)
    br1 = bp1.add_run("EMBEDDED CYBERSECURITY, IOT WIRELESS SYSTEMS & USB HID RESEARCH REPORT")
    br1.font.name = "Segoe UI"
    br1.font.size = Pt(8.5)
    br1.font.bold = True
    br1.font.color.rgb = RGBColor(0x5E, 0xEA, 0xD4)

    bp2 = bcell.add_paragraph()
    bp2.paragraph_format.space_before = Pt(0)
    bp2.paragraph_format.space_after = Pt(3)
    br2 = bp2.add_run(
        "ESP32-S3 Phone-Controlled USB HID Keyboard and Mouse with BadUSB Simulation and Defensive Keystroke Firewall"
    )
    br2.font.name = "Segoe UI"
    br2.font.size = Pt(15.5)
    br2.font.bold = True
    br2.font.color.rgb = RGB_WHITE

    bp3 = bcell.add_paragraph()
    bp3.paragraph_format.space_before = Pt(0)
    bp3.paragraph_format.space_after = Pt(0)
    br3 = bp3.add_run(
        "Native Composite TinyUSB Emulation, Dual-Mode Wi-Fi Mobile Web Controller, Deterministic Scenario State Machine & Win32 Hook Defense"
    )
    br3.font.name = "Segoe UI"
    br3.font.size = Pt(9.0)
    br3.font.italic = True
    br3.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

    # Student & Institutional Metadata Table
    add_section_h2(doc, "Project Identity & Academic Attribution", space_before=3, space_after=1.5)
    meta_tbl = doc.add_table(rows=2, cols=4)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_tbl.autofit = False
    set_table_borders(meta_tbl, HEX_BORDER)
    meta_widths = [26, 62, 28, 62]
    meta_data = [
        ("Authors:", "Ram Karthik G & Harini V", "Roll Number:", "CH.SC.U4CYS23037 & CH.SC.U4CYS23010"),
        ("Department:", "Cybersecurity", "Institution:", "Amrita Vishwa Vidyapeetham, Chennai"),
    ]
    for r_i, r_vals in enumerate(meta_data):
        row = meta_tbl.rows[r_i]
        prevent_row_split(row)
        for c_i, val in enumerate(r_vals):
            cell = row.cells[c_i]
            cell.width = Mm(meta_widths[c_i])
            set_cell_background(cell, HEX_BG_LIGHT if c_i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=40, bottom=40, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)
            r.font.bold = (c_i % 2 == 0) or (r_i == 0 and c_i == 1)
            r.font.color.rgb = RGB_NAVY_PRIMARY if c_i % 2 == 0 else RGB_TEXT_MAIN

    # Executive Summary Heading & Narrative
    add_section_h2(doc, "Executive Summary & Architectural Overview", space_before=4, space_after=1.5)
    add_body_p(
        doc,
        "Modern operating systems implicitly trust USB Human Interface Devices (HID) the moment they enumerate on the host bus. "
        "While this zero-configuration trust model enables universal plug-and-play usability, it exposes a severe physical-layer attack vector "
        "known as BadUSB, in which a programmable microcontroller impersonates a composite keyboard and mouse to inject rapid OS commands. "
        "Conversely, legitimate wireless remote input solutions typically require installing proprietary receiver software on the host PC, "
        "limiting deployment on locked-down laboratory or presentation workstations.",
        space_after=2.5,
    )
    add_body_p(
        doc,
        "This project engineers and validates a unified offensive-and-defensive embedded cybersecurity platform built on the Espressif ESP32-S3 SoC "
        "and a companion Windows Host Keystroke Firewall. Using the native USB OTG peripheral (GPIO 19 D- / GPIO 20 D+) and the TinyUSB stack, "
        "the ESP32-S3 enumerates simultaneously as a composite Boot Keyboard and 3-button Scroll Mouse while hosting a responsive dark-mode Single-Page "
        "Application (SPA) from flash memory (PROGMEM) over dual-mode Wi-Fi (WIFI_AP_STA). An operator using an Android smartphone can launch or abort "
        "four non-destructive security awareness scenarios, type on a full 6-row virtual keyboard with hardware modifier latching, control the host cursor "
        "via a 60 Hz multi-touch trackpad, and demonstrate real-time host mitigation using a Python WH_KEYBOARD_LL low-level input suppression firewall.",
        space_after=2.5,
    )

    add_figure_block(
        doc,
        "cover_banner.png",
        "Figure 1.1: End-to-End Platform Architecture bridging the Mobile Web SPA, ESP32-S3 Native Composite TinyUSB Core, and Windows Host Firewall.",
        width_mm=174,
        space_before=1.5,
        space_after=2,
    )

    t1_headers = ["Subsystem Domain", "Implemented Engineering Mechanism", "Verified Hardware / QA Metric"]
    t1_rows = [
        ("Composite USB HID", "TinyUSB USBHIDKeyboard + USBHIDMouse on GPIO 19/20", "Zero-driver enumeration; 3.5 s boot guard; [-127, 127] clamping"),
        ("Dual-Mode Wireless", "WIFI_AP_STA (192.168.4.1 SoftAP + 2.4 GHz Hotspot STA) + mDNS", "Live phone access via 10.85.248.29 & http://badusb.local"),
        ("Scenario Engine FSM", "8-state non-blocking FSM + portMUX_TYPE spinlock mailbox", "Auto-runs Scenario 1 on boot; GPIO 0 cycles 1->2->3->4->1"),
        ("Remote Keyboard & Mouse", "4 keyboard sub-views, latched modifiers, 60 Hz multi-touch pad", "1-finger move/tap, 2-finger scroll/R-click, drag lock, 256B guard"),
        ("Emergency Abort Safety", "Cooperative 10 ms smartDelay polling + dual HID releaseAll()", "<= 10 ms abort latency; zero stuck modifiers or mouse buttons"),
        ("Host Keystroke Defense", "Python WH_KEYBOARD_LL hook (suppress=True) + 15 s watchdog", "Blocks injected keys globally; auto-disarms after 15.0 seconds"),
        ("Firmware & QA Validation", "Compiled for esp32:esp32:esp32s3 (hwcdc); 3 automated test suites", "851,520 B Flash (64.9%), 59,496 B RAM (18.1%); 22/22 tests pass"),
    ]
    add_styled_table(
        doc,
        t1_headers,
        t1_rows,
        [36, 74, 68],
        caption_text="Table 1.1: Summary of Core Platform Subsystems, Implementation Mechanisms, and Verified Metrics",
        font_size=7.9,
        cell_pad_v=30,
        space_before=1,
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: SECTION 1 — ABSTRACT, PROBLEM STATEMENT & OBJECTIVES
    # =========================================================================
    add_section_h1(doc, "01", "Abstract, Problem Statement & Objectives", space_before=0, space_after=3)

    add_section_h2(doc, "1.1 Background and the USB HID Trust Model", space_before=2, space_after=1.5)
    add_body_p(
        doc,
        "Universal Serial Bus (USB) Human Interface Devices represent the primary physical trust boundary between human operators and modern computing platforms. "
        "When a peripheral is connected to a USB host port, the operating system reads its USB Device, Configuration, Interface, and HID Report Descriptors. "
        "Whenever an interface declares USB Class 0x03 (HID), Subclass 0x01 (Boot Interface), and Protocol 0x01 (Keyboard) or 0x02 (Mouse), the host OS kernel "
        "automatically binds built-in class drivers (kbdclass.sys and mouclass.sys on Windows) without requiring driver signatures, user confirmation dialogs, "
        "or cryptographic device authentication.",
        space_after=2.5,
    )
    add_body_p(
        doc,
        "As first formalized by Nohl and Lell in their seminal BadUSB research, the operating system has no native architectural mechanism at the USB HID layer "
        "to distinguish electrical scancodes generated by a physical mechanical switch from synthetic HID reports generated by an embedded microcontroller timer. "
        "A microcontroller capable of native USB device emulation can therefore open command shells (`Win + R`), execute administrative utilities, or manipulate "
        "cursor coordinates at hundreds of characters per second.",
        space_after=2.5,
    )

    add_section_h2(doc, "1.2 Problem Statement & Academic Motivation", space_before=3, space_after=1.5)
    add_body_p(
        doc,
        "Despite the pedagogical importance of demonstrating physical USB security risks in university cybersecurity curricula, existing hardware tools exhibit "
        "three critical engineering shortcomings that hinder safe classroom instruction and practical multi-role use:",
        space_after=2,
    )
    add_bullet_p(
        doc,
        "Blind, Non-Interruptible Static Execution: ",
        "Conventional BadUSB demonstration boards execute hardcoded keystroke arrays immediately upon USB insertion. They provide no wireless status feedback, "
        "no runtime scenario switching, and no emergency abort mechanism if the target window fails to open in time.",
    )
    add_bullet_p(
        doc,
        "Host Agent Dependency in Wireless Input Tools: ",
        "Standard smartphone-to-PC remote keyboard and mouse applications require installing a background TCP/UDP server daemon on the target computer. "
        "In restricted academic laboratories, smart classrooms, or hardware debugging benches, installing third-party host agents is disallowed.",
    )
    add_bullet_p(
        doc,
        "Lack of Integrated Defensive Countermeasures: ",
        "Demonstrating offensive keystroke injection without a companion host-side mitigation leaves students without actionable defensive engineering patterns, "
        "while naive keyboard hooks risk locking out the instructor's physical keyboard if not paired with an automated fail-safe timer.",
        space_after=2.5,
    )

    add_section_h2(doc, "1.3 Core Research and Engineering Objectives", space_before=3, space_after=1.5)
    add_figure_block(
        doc,
        "objectives_diagram.png",
        "Figure 1.2: Four-Pillar Research and Engineering Objectives Matrix with Verified Hardware & Test Milestones.",
        width_mm=174,
        space_before=1,
        space_after=2.5,
    )

    add_section_h2(doc, "1.4 Scope, Safety Boundaries, and Ethical Design", space_before=2, space_after=1.5)
    add_body_p(
        doc,
        "This system is strictly scoped as an authorized educational demonstration platform, wireless driverless HMI peripheral, and defensive endpoint security "
        "testbed. Rigorous engineering safeguards are enforced across both firmware and host software:",
        space_after=2,
    )
    add_bullet_p(
        doc,
        "Non-Destructive Educational Scenarios Only: ",
        "None of the four embedded scenarios delete files, modify system registries, exfiltrate credentials, or establish persistence. Scenario 3 displays an "
        "educational awareness notice inside Notepad, and Scenario 4 lists saved Wi-Fi SSID names (`netsh wlan show profiles`) without reading key material.",
    )
    add_bullet_p(
        doc,
        "Credential Redaction & Input Bounding: ",
        "All Wi-Fi station passphrases, SoftAP passwords, authentication PINs, and device serial numbers are redacted as `[REDACTED]` in documentation and masked "
        "in the mobile UI (`•••••••••`). Bulk text transmission is bounded to `MAX_TEXT_LENGTH = 256` characters per request.",
        space_after=3,
    )

    add_callout_box(
        doc,
        "ARCHITECTURAL CONVERGENCE:",
        "By combining a composite TinyUSB HID engine, an embedded PROGMEM web application, a deterministic 8-state scenario FSM, and a Win32 WH_KEYBOARD_LL "
        "firewall within a single repository, the platform serves simultaneously as a daily-use wireless mobile keyboard/trackpad and a controlled cybersecurity lab.",
        accent_hex=HEX_TEAL_ACCENT,
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: SECTION 2 — SYSTEM ARCHITECTURE & TECHNOLOGY STACK
    # =========================================================================
    add_section_h1(doc, "02", "System Architecture & Technology Stack", space_before=0, space_after=3)

    add_section_h2(doc, "2.1 End-to-End Three-Tier System Architecture", space_before=2, space_after=1.5)
    add_body_p(
        doc,
        "The platform architecture is partitioned into three decoupled tiers that communicate over standard protocols: (1) the Android Phone Controller Tier "
        "(rendering the Single-Page Application over HTTP REST JSON), (2) the ESP32-S3 Embedded Firmware Tier (managing dual-mode Wi-Fi, token validation, "
        "the thread-safe Scenario FSM, and composite TinyUSB HID report generation), and (3) the Windows Host & Firewall Tier (enumerating the composite USB "
        "device and filtering input events via the Win32 low-level keyboard hook chain).",
        space_after=2,
    )

    add_figure_block(
        doc,
        "system_architecture.png",
        "Figure 2.1: Complete Three-Tier System Architecture illustrating Mobile SPA Tabs, ESP32-S3 Firmware Modules, and Windows Host Firewall Pipeline.",
        width_mm=158,
        space_before=1,
        space_after=2.5,
    )

    add_section_h2(doc, "2.2 Dual-Mode Wi-Fi Topology and Native USB OTG Interfacing", space_before=2, space_after=1.5)
    add_body_p(
        doc,
        "A foundational hardware distinction of the Espressif ESP32-S3 over legacy ESP32-WROOM modules is its integrated full-speed (12 Mbps) USB 2.0 On-The-Go "
        "(OTG) peripheral controller routed directly to GPIO 19 (`USB D-`) and GPIO 20 (`USB D+`). When compiled with Arduino-ESP32 TinyUSB configuration flags "
        "(`USBMode=hwcdc,CDCOnBoot=cdc`), the ESP32-S3 presents a composite USB descriptor over a single USB data cable that simultaneously binds three host "
        "interfaces: USB CDC Serial (`COM5` for telemetry and flashing), a standard 104-key USB HID Boot Keyboard, and a 3-button USB HID Mouse with vertical scroll.",
        space_after=2,
    )
    add_body_p(
        doc,
        "On the wireless side, `WebServerHandler::begin()` configures the IEEE 802.11 b/g/n radio in concurrent `WIFI_AP_STA` mode. The SoftAP interface "
        "immediately establishes an isolated control network (`SSID: BadUSB-Controller`, Passphrase: `[REDACTED]`, Static IP: `192.168.4.1`), while the Station "
        "interface connects automatically to the user's 2.4 GHz mobile hotspot (`SSID: [REDACTED]`, Passphrase: `[REDACTED]`, assigned DHCP IP `10.85.248.29`). "
        "Because the smartphone hosts the 2.4 GHz hotspot, the phone browser can communicate directly with `http://10.85.248.29` (or `http://badusb.local` via mDNS) "
        "without disconnecting from mobile cellular data.",
        space_after=2.5,
    )

    t2_headers = ["Architectural Layer", "File / Module", "Key Classes, Libraries & Technical Responsibilities"]
    t2_rows = [
        ("Main Firmware Entry", "badusb_firmware.ino", "Initializes Serial (115200), ScenarioController, WebServerHandler, and cooperative loop()"),
        ("System Configuration", "config.h", "Defines WIFI_AP/STA credentials [REDACTED], AUTH_PIN [REDACTED], GPIO 0 pin, and timing guards"),
        ("HID Keyboard Engine", "keyboard_controller.h/.cpp", "Wraps USBHIDKeyboard; ASCII typing, named keys, modifier bitmasks, shortcuts, releaseAll()"),
        ("HID Mouse Engine", "mouse_controller.h/.cpp", "Wraps USBHIDMouse; clamped [-127, 127] relative move, L/R/M click, drag press/release, scroll"),
        ("Scenario State Machine", "scenario_controller.h/.cpp", "8-state FSM, portMUX_TYPE spinlock command mailbox, GPIO 0 debounce, Scenarios 1–4"),
        ("HTTP REST Server", "web_server_handler.h/.cpp", "Port 80 WebServer, WIFI_AP_STA setup, X-Auth-Token checks, CORS preflight, 13 API routes"),
        ("Embedded Mobile SPA", "web_assets.h (PROGMEM)", "Responsive dark-mode HTML5/CSS3/JS interface: Scenarios, 4-View Keyboard, Touchpad, Settings"),
        ("Host Keystroke Firewall", "src/firewall.py & firewall.py", "Python 3.12 Tkinter GUI, keyboard.hook(suppress=True) WH_KEYBOARD_LL filter, 15s Timer"),
    ]
    add_styled_table(
        doc,
        t2_headers,
        t2_rows,
        [35, 42, 101],
        caption_text="Table 2.1: Repository Module Breakdown and Architectural Responsibilities Verified Against Source Code",
        font_size=7.8,
        cell_pad_v=26,
        space_before=1,
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: SECTION 3 — EMBEDDED FIRMWARE & SCENARIO EXECUTION ENGINE
    # =========================================================================
    add_section_h1(doc, "03", "Embedded Firmware & Scenario Execution Engine", space_before=0, space_after=3)

    add_section_h2(doc, "3.1 Composite USB Initialization Ordering & Enumeration Guard", space_before=2, space_after=1.5)
    add_body_p(
        doc,
        "TinyUSB requires all HID report descriptors to be registered before the physical USB bus attaches to the host. Inside `ScenarioController::begin()`, "
        "the firmware calls `keyboard.begin()` (`USBHIDKeyboard::begin()`) and `mouse.begin()` (`USBHIDMouse::begin()`) prior to invoking `USB.begin()`. "
        "Once `USB.begin()` asserts the D+ pull-up resistor on GPIO 20, the host OS initiates USB enumeration. Because Windows takes 1.5 to 3.0 seconds to "
        "complete descriptor negotiation and ready the HID input queues, the FSM enters `STATE_USB_WAIT` and enforces a non-blocking 3,500 ms stabilization "
        "window (`USB_READY_WAIT_MS = 3500`) before permitting any automated or remote HID transmission.",
        space_after=2.5,
    )

    add_section_h2(doc, "3.2 Deterministic 8-State Finite State Machine & Spinlock Synchronization", space_before=2.5, space_after=1.5)
    add_body_p(
        doc,
        "To guarantee predictable behavior across boot-time execution, physical button presses, and asynchronous web requests, `ScenarioController` implements "
        "an 8-state FSM (`STATE_BOOTING`, `STATE_USB_WAIT`, `STATE_STARTUP_PAYLOAD`, `STATE_IDLE`, `STATE_RUNNING`, `STATE_STOPPING`, `STATE_STOPPED`, and "
        "`STATE_ERROR`). External triggers never mutate state variables directly; instead, they queue a command (`CMD_SELECT_SCENARIO`, `CMD_NEXT_SCENARIO`, "
        "or `CMD_STOP`) inside an ESP-IDF FreeRTOS critical section (`portENTER_CRITICAL(&mux)` / `portEXIT_CRITICAL(&mux)`). When the 3,500 ms boot wait "
        "completes, `STATE_STARTUP_PAYLOAD` automatically runs Scenario 1 once (`startupPending = false; startupDone = true`) and transitions to `STATE_IDLE`.",
        space_after=2,
    )

    add_figure_block(
        doc,
        "fsm_diagram.png",
        "Figure 3.1: ScenarioController 8-State Finite State Machine (FSM) and Interrupt-Safe Execution Flow.",
        width_mm=170,
        space_before=1,
        space_after=2.5,
    )

    add_section_h2(doc, "3.3 Physical GPIO 0 BOOT Button Advancement & Cooperative Abort Safety", space_before=2, space_after=1.5)
    add_body_p(
        doc,
        "The ESP32-S3 onboard `BOOT` button (`GPIO 0`, active-low with internal pull-up) is polled on every `ScenarioController::update()` cycle. Raw readings "
        "pass through a 50 ms debounce filter (`BUTTON_DEBOUNCE_MS = 50`) and a 600 ms post-trigger cooldown (`BUTTON_COOLDOWN_MS = 600`). Pressing the button "
        "invokes `requestNextScenario()`, which computes `(currentScenario % 4) + 1`, advancing circularly through Scenarios `1 -> 2 -> 3 -> 4 -> 1`.",
        space_after=2,
    )
    add_body_p(
        doc,
        "During scenario execution, all inter-step pauses use `ScenarioController::smartDelay(unsigned long ms)`. Rather than blocking the CPU, `smartDelay` "
        "loops in 10 ms increments (`STEP_POLL_INTERVAL_MS = 10`), invoking the registered client callback (`webHandler.handleClient()`) and checking "
        "`stopRequested` on every iteration. During live hardware QA, a critical deadlock defect was discovered and resolved in `requestStop()`: "
        "calling `keyboard.releaseAll()` inside `portENTER_CRITICAL(&mux)` previously stalled the TinyUSB task while interrupts were disabled. "
        "Moving `keyboard.releaseAll()` and `mouse.releaseAll()` outside the spinlock critical section achieved instantaneous, crash-free aborts.",
        space_after=2.5,
    )

    t3_headers = ["ID", "Scenario Title", "Exact HID Sequence Executed on Host", "Security Awareness Objective"]
    t3_rows = [
        ("1", "Notepad Awareness (Boot Auto-Run)", "GUI+r (Win+R) -> wait 750ms -> type 'notepad' + Enter -> wait 1200ms -> type 3-line security warning message", "Demonstrates how unattended USB ports allow immediate process creation and text injection."),
        ("2", "Portal Redirection", "GUI+r (Win+R) -> wait 750ms -> type 'cmd' + Enter -> wait 1000ms -> type 'start https://intranet.cb.amrita.edu/' + Enter", "Demonstrates forced browser navigation and potential credential phishing via command shell."),
        ("3", "Ransomware Awareness", "GUI+r (Win+R) -> wait 750ms -> type 'notepad' + Enter -> wait 1200ms -> type '[ SECURITY EDUCATION NOTICE ]' banner", "Safely simulates rapid payload staging visibility in a classroom without modifying user files."),
        ("4", "Wi-Fi Reconnaissance", "GUI+r (Win+R) -> wait 750ms -> type 'cmd' + Enter -> wait 1000ms -> execute 'netsh wlan show profiles' in console", "Shows how local system enumeration commands can list saved wireless network profile names."),
    ]
    add_styled_table(
        doc,
        t3_headers,
        t3_rows,
        [10, 38, 68, 62],
        caption_text="Table 3.1: Verified Catalog of Non-Destructive Educational Scenarios Implemented in scenario_controller.cpp",
        font_size=7.9,
        cell_pad_v=30,
        space_before=1,
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 5: SECTION 4 — WI-FI PHONE CONTROLLER & REMOTE KEYBOARD
    # =========================================================================
    add_section_h1(doc, "04", "Wi-Fi Phone Controller & Remote Keyboard", space_before=0, space_after=3)

    add_section_h2(doc, "4.1 Embedded PROGMEM Single-Page Application & Live Telemetry", space_before=2, space_after=1.5)
    add_body_p(
        doc,
        "The mobile web interface is compiled directly into the firmware binary inside `badusb_firmware/web_assets.h` as a `PROGMEM` string literal (`INDEX_HTML`). "
        "By avoiding external CSS frameworks or CDN scripts, the interface loads instantaneously over both the standalone SoftAP (`192.168.4.1`) and the phone's "
        "2.4 GHz hotspot (`10.85.248.29`). During live Android QA on the Vivo V50e (`chrome://inspect` over ADB), an unclosed `<div id=\"tabKeyboard\">` container "
        "bug that previously hid the Mouse and Settings tabs was identified and fixed, along with adding explicit CORS `HTTP_OPTIONS` preflight support (`204 No Content`).",
        space_after=2,
    )

    add_section_h2(doc, "4.2 Token-Based Authentication and REST API Command Flow", space_before=2.5, space_after=1.5)
    add_body_p(
        doc,
        "To prevent unauthorized users on the same Wi-Fi subnet from injecting keystrokes, all state-modifying `POST` routes require authentication. "
        "In the Settings tab, the operator inputs the configured security PIN (`[REDACTED]`), which is verified via `POST /api/auth/login` against `AUTH_PIN` "
        "in `config.h`. Once authenticated, the client attaches `X-Auth-Token: [REDACTED]` to all `fetch()` requests. `WebServerHandler::isAuthorized()` "
        "validates this header before executing any scenario, keyboard, or mouse action, returning HTTP `401 Unauthorized` if missing or invalid.",
        space_after=2,
    )

    add_section_h2(doc, "4.3 Four-Sub-View Remote Keyboard, Modifiers & Shortcuts", space_before=2.5, space_after=1.5)
    add_body_p(
        doc,
        "The Keyboard tab (`#tabKeyboard`) replicates a complete desktop keyboard on the smartphone touchscreen through a persistent Hardware Modifier bar "
        "(`Ctrl`, `Alt`, `Shift`, `Win` with `Auto-release modifier` and `Release All` safety controls) and four specialized sub-views: "
        "(1) `Full Layout` (6-row desktop matrix including `Esc`, `F1`–`F12`, `Del`, symbol/number row, `Tab`, `Caps Lock`, `Shift`, `Win`, `Alt`, `Menu`, and `Spacebar`), "
        "(2) `Shortcuts` (one-tap macros such as `Copy`, `Paste`, `Task Manager`, `Win+R`, `Win+D`, `Win+L`, `Alt+F4`, and an inverted-T arrow/page navigation cluster), "
        "(3) `Text & Live` (256-character bulk string transmitter and real-time per-keystroke live input box), and (4) `Numpad` (17-key numeric keypad).",
        space_after=2,
    )

    add_figure_block(
        doc,
        "phone_ui_scenarios_keyboard.png",
        "Figure 4.1: Verified Live Android Phone Screenshots — (a) Educational Scenarios & Direct Launch Tab; (b) Full 6-Row Hardware Keyboard & Modifier Bar.",
        width_mm=84,
        space_before=1,
        space_after=1.5,
    )

    t4_headers = ["HTTP Method & Route", "Auth", "Request Payload Parameters", "Firmware Handler & HID Action"]
    t4_rows = [
        ("GET /api/status", "Public", "None", "Returns JSON: usbReady, state, currentScenario, staIp, apIp, authRequired"),
        ("POST /api/auth/login", "Public", "pin / token ([REDACTED])", "Verifies credential against AUTH_PIN; returns 200 OK or 401 Unauthorized"),
        ("POST /api/scenario/select", "Token", "id (integer 1..4)", "Queues CMD_SELECT_SCENARIO in spinlock mailbox to launch Scenario 1–4"),
        ("POST /api/scenario/next", "Token", "None", "Queues CMD_NEXT_SCENARIO; advances circularly 1 -> 2 -> 3 -> 4 -> 1"),
        ("POST /api/scenario/stop", "Token", "None", "Sets stopRequested=true, aborts smartDelay(), calls Keyboard/Mouse releaseAll()"),
        ("POST /api/keyboard/key", "Token", "key (e.g. ENTER, F5, a)", "Maps key name to USB HID usage code via KeyboardController::sendKeyByName()"),
        ("POST /api/keyboard/shortcut", "Token", "mod (CTRL+SHIFT), key (ESC)", "Presses modifier bitmask + target key for 25 ms, then releases cleanly"),
        ("POST /api/keyboard/text", "Token", "text (<=256B), enter (0/1)", "Streams printable ASCII characters via Keyboard.print() + optional Enter"),
    ]
    add_styled_table(
        doc,
        t4_headers,
        t4_rows,
        [40, 13, 41, 84],
        caption_text="Table 4.1: Core Status, Authentication, Scenario, and Keyboard REST API Endpoints (web_server_handler.cpp)",
        font_size=7.6,
        cell_pad_v=18,
        space_before=1,
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 6: SECTION 5 — REMOTE MOUSE CONTROL & HOST-SIDE DEFENSE
    # =========================================================================
    add_section_h1(doc, "05", "Remote Mouse Control & Host-Side Defense", space_before=0, space_after=3)

    add_section_h2(doc, "5.1 Multi-Touch Relative Trackpad, Gestures & Precision Nudge", space_before=2, space_after=1.5)
    add_body_p(
        doc,
        r"The Mouse tab (`#tabMouse`) implements a low-latency wireless touchpad backed by `MouseController` (`mouse_controller.h/.cpp`). Touch coordinates "
        r"on `#trackpadArea` are sampled via `touchstart`, `touchmove`, and `touchend` listeners throttled to 16 ms intervals (~60 Hz). Single-finger movement "
        r"calculates relative (dx, dy) offsets scaled by the Cursor Sensitivity slider (`0.5x`–`3.0x`, default `1.8x`) and clamped to signed 8-bit "
        r"HID integers (`[-127, 127]`) inside `MouseController::clampDelta()`. A single-finger tap (<10 px movement within 220 ms) triggers a "
        r"Left Click, while a two-finger tap (<260 ms) triggers a Right Click and a two-finger vertical drag emulates the scroll wheel (`POST /api/mouse/scroll`). "
        r"Dedicated buttons provide Left, Right, Double, and Middle Click, alongside a stateful `Drag Lock` toggle (`POST /api/mouse/press` and `/release`) and "
        r"a Precision Nudge pad (`5px`, `20px`, `60px` step selector).",
        space_after=2,
    )

    add_figure_block(
        doc,
        "phone_ui_mouse_settings.png",
        "Figure 5.1: Verified Live Android Phone Screenshots — (a) Multi-Touch Trackpad, Click Bar & Drag Lock; (b) Masked PIN Auth & Dual-Mode Network Telemetry.",
        width_mm=84,
        space_before=1,
        space_after=2,
    )

    add_section_h2(doc, "5.2 Windows Host-Side Keystroke Firewall Architecture", space_before=2, space_after=1.5)
    add_body_p(
        doc,
        "To demonstrate practical host-side defense against unauthorized HID keystroke injection, the platform includes a Python/Tkinter desktop security "
        "utility (`src/firewall.py`). When toggled from `ALLOW (Monitoring)` to `BLOCKING (Armed)` mode, `KeystrokeFirewall.enable_blocking()` installs a "
        "Win32 low-level keyboard hook (`WH_KEYBOARD_LL`) with `keyboard.hook(self._on_key_event, suppress=True)`. Because `WH_KEYBOARD_LL` executes in the "
        "global OS input chain prior to foreground window routing, returning with `suppress=True` drops all incoming keystrokes from both automated BadUSB "
        "scenarios and remote typing. To guarantee that the operator is never permanently locked out of their PC, arming the hook starts a 15.0-second watchdog "
        "`threading.Timer(15.0, self._auto_disarm)` and registers `atexit` / `WM_DELETE_WINDOW` cleanup handlers that invoke `keyboard.unhook_all()`.",
        space_after=2,
    )

    add_figure_block(
        doc,
        "defense_architecture.png",
        "Figure 5.2: Windows Host Keystroke Firewall Interception Pipeline (WH_KEYBOARD_LL Hook, Suppression Gate, and 15s Fail-Safe Watchdog).",
        width_mm=164,
        space_before=1,
        space_after=2,
    )

    t5_headers = ["Comparison Criterion", "Implemented Host Firewall (WH_KEYBOARD_LL)", "Hardware / Kernel USB Device Filtering"]
    t5_rows = [
        ("Operating System Layer", "User-Space Win32 Hook Chain (SetWindowsHookEx)", "Kernel-Mode USB Bus / Filter Driver (WDF / udev)"),
        ("Suppression Granularity", "Global: Suppresses all keyboard scancodes system-wide", "Per-Device: Filters by USB Vendor/Product ID or port"),
        ("Resilience to VID/PID Spoofing", "High: Blocks keystrokes even if BadUSB spoofs Dell/Logitech IDs", "Low: Bypassed when attacker clones an authorized VID/PID"),
        ("Fail-Safe Lockout Protection", "Built-in 15.0s auto-disarm watchdog + clean exit unhook", "Requires safe-mode boot if primary keyboard is blacklisted"),
    ]
    add_styled_table(
        doc,
        t5_headers,
        t5_rows,
        [42, 68, 68],
        caption_text="Table 5.1: Architectural Tradeoffs Between User-Space Global Hook Suppression and Kernel USB Device Filtering",
        font_size=7.8,
        cell_pad_v=24,
        space_before=1,
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 7: SECTION 6 — TESTING, RESULTS & TECHNICAL VALIDATION
    # =========================================================================
    add_section_h1(doc, "06", "Testing, Results & Technical Validation", space_before=0, space_after=2.5)

    add_section_h2(doc, "6.1 Multi-Tier Verification Methodology (Simulation, Unit & Live Hardware)", space_before=1.5, space_after=1.5)
    add_body_p(
        doc,
        "A rigorous three-stage verification methodology was executed to validate every firmware module, mobile UI view, REST endpoint, and host firewall behavior. "
        "First, behavioral simulation and unit test suites (`tests/test_controller_simulation.py` and `tests/test_firewall.py`) verified the 8-state FSM, circular "
        "scenario progression, token authentication, mouse coordinate clamping, and `WH_KEYBOARD_LL` suppression/watchdog timers. Second, the firmware was compiled "
        "via `arduino-cli` (`esp32:esp32:esp32s3:USBMode=hwcdc,CDCOnBoot=cdc`) and flashed over `COM5` (`851,520 bytes`). Third, an Android phone (`Vivo V50e`, "
        "Android 16, serial `[REDACTED]`) was connected over ADB and inspected via Chrome DevTools Protocol (`tests/test_live_phone_api.py`), executing 10 live "
        "end-to-end API and DOM verification tests directly from the mobile browser against the physical ESP32-S3 at `http://10.85.248.29/`.",
        space_after=2,
        font_size=8.8,
    )

    t6_headers = ["Test Suite", "Automated Test Case Identifier", "Verified Engineering Requirement & Behavior", "Status"]
    t6_rows = [
        ("Controller Sim", "test_boot_runs_scenario_1_automatically", "3.5s USB enumeration guard + Scenario 1 auto-execution on boot", "PASS"),
        ("Controller Sim", "test_button_cycles_1_to_4_and_wraps", "GPIO 0 button advances circularly 1 -> 2 -> 3 -> 4 -> 1", "PASS"),
        ("Controller Sim", "test_direct_scenario_selection_and_validation", "Direct launch of Scenarios 1..4; HTTP 400 on invalid ID 99", "PASS"),
        ("Controller Sim", "test_stop_interrupts_and_releases_keys", "Emergency stop aborts running scenario & calls releaseAll()", "PASS"),
        ("Controller Sim", "test_authentication_protection", "Rejects unauthenticated POST (401); accepts valid X-Auth-Token", "PASS"),
        ("Controller Sim", "test_keyboard_text_and_special_keys", "ASCII typing, 256-char limit enforcement, and named special keys", "PASS"),
        ("Controller Sim", "test_shortcuts_and_modifier_release", "Composite CTRL+c shortcut press/release and modifier clear", "PASS"),
        ("Controller Sim", "test_mouse_move_click_drag_and_scroll", "Delta clamping [-127, 127], L/R/M click, drag lock, scroll wheel", "PASS"),
        ("Host Firewall", "test_initial_state_is_allow", "Firewall initializes in ALLOW state with no active keyboard hook", "PASS"),
        ("Host Firewall", "test_enable_blocking_installs_suppressive_hook", "Arms WH_KEYBOARD_LL hook with suppress=True + 15s watchdog", "PASS"),
        ("Host Firewall", "test_disable_blocking_unhooks_cleanly", "Disarms hook cleanly and cancels active threading.Timer", "PASS"),
        ("Host Firewall", "test_auto_disarm_safety_timeout", "Watchdog callback automatically restores ALLOW mode after 15.0s", "PASS"),
        ("Live Phone API", "test_01_ui_tabs_and_containers_present", "Phone Chrome DOM renders all 4 main tabs & 4 keyboard sub-tabs", "PASS"),
        ("Live Phone API", "test_02_status_endpoint_live", "Live GET /api/status returns usbReady:true, staIp:10.85.248.29", "PASS"),
        ("Live Phone API", "test_03_auth_enforcement", "Live unauthenticated POST from phone receives HTTP 401", "PASS"),
        ("Live Phone API", "test_04_auth_login_valid", "Live POST /api/auth/login with valid PIN returns 200 OK", "PASS"),
        ("Live Phone API", "test_05_keyboard_special_keys_and_modifiers", "Live phone dispatch of SPACE, BACKSPACE, CTRL+c, and release", "PASS"),
        ("Live Phone API", "test_06_keyboard_bulk_text_validation", "Live bulk text injection (200) and >256 char rejection (400)", "PASS"),
        ("Live Phone API", "test_07_mouse_move_click_drag_scroll_release", "Live phone cursor move, L/R/double click, drag lock, and scroll", "PASS"),
        ("Live Phone API", "test_08_scenario_select_and_emergency_stop", "Live launch of Scenario 4 followed by immediate /api/scenario/stop", "PASS"),
        ("Live Phone API", "test_09_invalid_inputs_rejected_cleanly", "Live HTTP 400 validation for scenario ID 99 & unknown key name", "PASS"),
        ("Live Phone API", "test_10_cors_preflight_options", "Live OPTIONS request returns 204 No Content with CORS headers", "PASS"),
    ]
    add_styled_table(
        doc,
        t6_headers,
        t6_rows,
        [23, 68, 73, 14],
        caption_text="Table 6.1: Complete Automated & Live Hardware Verification Matrix (22 / 22 Tests Passed)",
        font_size=7.4,
        cell_pad_v=20,
        space_before=1,
    )

    t7_headers = ["Firmware / Hardware Resource Metric", "Measured Value", "Target Partition / Limit", "Utilization / Engineering Notes"]
    t7_rows = [
        ("Compiled Flash Binary Size", "851,520 bytes", "1,310,720 bytes", "64.9% of app partition (TinyUSB + Wi-Fi + PROGMEM UI)"),
        ("Global Dynamic SRAM Allocation", "59,496 bytes", "327,680 bytes", "18.1% of internal RAM (268,184 bytes free for heap/stack)"),
        ("Boot-to-HID Enumeration Guard", "3,500 ms", "Configurable (config.h)", "Prevents dropped keystrokes during initial USB bus reset"),
        ("Emergency Stop Preemption Latency", "<= 10 ms", "10 ms smartDelay slice", "Immediate scenario abort & dual HID releaseAll()"),
    ]
    add_styled_table(
        doc,
        t7_headers,
        t7_rows,
        [48, 28, 36, 66],
        caption_text="Table 6.2: ESP32-S3 Firmware Resource Utilization and Real-Time Timing Metrics",
        font_size=7.6,
        cell_pad_v=20,
        space_before=3,
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 8: SECTION 7 — LIMITATIONS, CONCLUSION, FUTURE WORK & REFERENCES
    # =========================================================================
    add_section_h1(doc, "07", "Limitations, Conclusion, Future Work & References", space_before=0, space_after=3)

    add_section_h2(doc, "7.1 Known Technical and Architectural Limitations", space_before=2, space_after=1.5)
    add_body_p(
        doc,
        "To maintain strict engineering transparency, four architectural boundaries of the current implementation are explicitly documented:",
        space_after=2,
    )
    add_bullet_p(
        doc,
        "Unidirectional US-ASCII / QWERTY HID Assumption: ",
        "Standard USB HID Boot Keyboards transmit unacknowledged scancodes assuming a US-English QWERTY host layout. Non-ASCII Unicode characters are skipped "
        "by `KeyboardController::typeText()`, and the ESP32-S3 has no bidirectional visibility into which host window holds focus.",
    )
    add_bullet_p(
        doc,
        "Cleartext Local HTTP Transport on Port 80: ",
        "Because mobile browsers block self-signed HTTPS certificates on dynamic private IPs (`192.168.4.1` or hotspot DHCP) without manual CA installation, "
        "the web controller uses unencrypted HTTP. While `X-Auth-Token` prevents unauthorized API execution, traffic is not encrypted against passive local sniffing.",
    )
    add_bullet_p(
        doc,
        "Synchronous Single-Client HTTP Polling: ",
        "Arduino's built-in `WebServer` processes requests synchronously on a single thread. Touchpad motion events are therefore throttled to ~60 Hz (`16 ms`) "
        "on the smartphone client to avoid TCP queue saturation during rapid cursor swipes.",
    )
    add_bullet_p(
        doc,
        "Global Scope of Win32 WH_KEYBOARD_LL Hook: ",
        "The Windows low-level hook (`keyboard.hook(suppress=True)`) intercepts all keyboard input globally at the OS level rather than filtering by a specific "
        "hardware USB Vendor/Product ID (`VID/PID`). During the 15-second blocking window, both BadUSB keystrokes and physical laptop keys are suppressed.",
        space_after=2.5,
    )

    add_section_h2(doc, "7.2 Technical Conclusion", space_before=2.5, space_after=1.5)
    add_body_p(
        doc,
        "This project successfully designed, implemented, debugged, and hardware-verified an end-to-end ESP32-S3 Phone-Controlled USB HID Keyboard, Mouse, and "
        "BadUSB Defense Platform. By unifying composite TinyUSB peripheral emulation (`USBHIDKeyboard` and `USBHIDMouse`), concurrent `WIFI_AP_STA` wireless "
        "networking, a deterministic 8-state scenario Finite State Machine, a four-tab mobile Single-Page Application, and a fail-safe `WH_KEYBOARD_LL` host "
        "keystroke firewall, the system bridges embedded IoT engineering and practical endpoint cybersecurity. Live verification on an ESP32-S3 (`COM5`) and "
        "an Android smartphone (`Vivo V50e`) confirmed 100% pass rates across all 22 automated simulation, unit, and live browser API tests.",
        space_after=2.5,
    )

    add_section_h2(doc, "7.3 Future Engineering Improvements", space_before=2.5, space_after=1.5)
    add_bullet_p(
        doc,
        "Asynchronous WebSockets & Embedded TLS (WSS/HTTPS): ",
        "Migrating from REST `POST` requests to persistent WebSocket frames over `ESPAsyncWebServer` with mbedTLS session encryption will reduce trackpad "
        "transport overhead and protect authentication tokens on shared wireless networks.",
    )
    add_bullet_p(
        doc,
        "Per-Device Raw Input Attribution & Cadence Anomaly Detection: ",
        "Enhancing `src/firewall.py` with the Windows Raw Input API (`GetRawInputDeviceInfo`) and inter-keystroke timing analysis (<5 ms automated injection "
        "vs. >40 ms human typing cadence) will allow selective blocking of suspect USB HID peripherals while leaving the primary laptop keyboard unaffected.",
    )
    add_bullet_p(
        doc,
        "Non-Volatile Scenario Storage & Multi-Locale Keymaps: ",
        "Storing user-defined educational scripts and international keyboard layouts (UK, DE, FR) inside ESP32-S3 LittleFS/NVS flash partitions will enable "
        "dynamic scenario authoring from the mobile browser without recompiling firmware.",
        space_after=2.5,
    )

    add_section_h2(doc, "7.4 References", space_before=2.5, space_after=1.5)
    refs = [
        "[1] USB Implementers Forum (USB-IF), \"Device Class Definition for Human Interface Devices (HID), Version 1.11,\" USB-IF Specification, 2001.",
        "[2] USB Implementers Forum (USB-IF), \"HID Usage Tables for Universal Serial Bus (USB), Version 1.4,\" USB-IF Technical Specification, 2022.",
        "[3] K. Nohl and J. Lell, \"BadUSB — On Accessories That Turn Evil,\" in Proc. Black Hat USA Security Briefings, Las Vegas, NV, USA, Aug. 2014.",
        "[4] Espressif Systems, \"ESP32-S3 Technical Reference Manual, Version 1.5,\" Espressif Systems, Shanghai, China, 2024.",
        "[5] Espressif Systems, \"Arduino Core for ESP32 — USBHIDKeyboard and USBHIDMouse API Reference (TinyUSB Stack),\" Version 3.x, 2024.",
        "[6] H. Thach, \"TinyUSB: An Open-Source Cross-Platform USB Host/Device Stack for Embedded Microcontrollers,\" Technical Documentation, 2024.",
        "[7] Microsoft Corporation, \"SetWindowsHookExA Function and LowLevelKeyboardProc (WH_KEYBOARD_LL) Callback Reference,\" Win32 API Docs, 2024.",
        "[8] BoppreH, \"Python keyboard Library: Global Event Hook and Suppression Architecture for Windows and Linux,\" Version 0.13.5, PyPI, 2023.",
    ]
    for ref in refs:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Mm(6)
        p.paragraph_format.first_line_indent = Mm(-6)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2.0)
        p.paragraph_format.line_spacing = 1.05
        r = p.add_run(ref)
        r.font.name = "Segoe UI"
        r.font.size = Pt(8.3)
        r.font.color.rgb = RGB_TEXT_MAIN

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(2)
    p_sp.paragraph_format.space_after = Pt(2)

    add_callout_box(
        doc,
        "VERIFICATION & ARCHIVAL SIGN-OFF:",
        "All firmware modules (badusb_firmware/), host keystroke firewall defenses (src/firewall.py), automated test suites (22/22 passed), "
        "and mobile UI views have been compiled, flashed to physical ESP32-S3 hardware (COM5), and verified end-to-end on Android (Vivo V50e). "
        "All sensitive credentials, tokens, and device serial numbers are redacted in compliance with institutional cybersecurity guidelines.",
        accent_hex=HEX_NAVY_PRIMARY,
    )

    doc.save(DOCX_PATH)
    print(f"Saved DOCX: {DOCX_PATH}")


def inject_lossless_4k_images_into_pdf():
    """
    Microsoft Word's PDF exporter downsamples embedded images to ~200 PPI.
    This post-processor replaces every embedded image XREF in the exported PDF
    directly with the uncompressed, lossless 4K (3960px / 3784px, 600 DPI) PNG
    from reports/assets/ so the PDF retains crystal-clear 4K visual sharpness.
    """
    page_asset_map = {
        0: ["cover_banner.png"],
        1: ["objectives_diagram.png"],
        2: ["system_architecture.png"],
        3: ["fsm_diagram.png"],
        4: ["phone_ui_scenarios_keyboard.png"],
        5: ["phone_ui_mouse_settings.png", "defense_architecture.png"],
    }
    pdf_doc = fitz.open(PDF_PATH)
    replaced_count = 0
    for page_idx, asset_names in page_asset_map.items():
        if page_idx >= len(pdf_doc):
            continue
        page = pdf_doc[page_idx]
        img_infos = page.get_image_info(xrefs=True)
        # Sort images top-to-bottom by their bounding box y0 coordinate
        img_infos_sorted = sorted(img_infos, key=lambda info: info["bbox"][1])
        # Deduplicate xrefs while preserving top-to-bottom order
        seen_xrefs = []
        for info in img_infos_sorted:
            xref = info.get("xref", 0)
            if xref and xref not in seen_xrefs:
                seen_xrefs.append(xref)

        for xref, asset_name in zip(seen_xrefs, asset_names):
            asset_path = os.path.join(ASSETS_DIR, asset_name)
            page.replace_image(xref, filename=asset_path)
            replaced_count += 1
            print(f"  Injected lossless 4K image on Page {page_idx + 1} (xref={xref}): {asset_name}")

    tmp_pdf = PDF_PATH + ".4k_tmp.pdf"
    pdf_doc.save(tmp_pdf, garbage=4, deflate=True)
    pdf_doc.close()
    os.replace(tmp_pdf, PDF_PATH)
    print(f"Completed lossless 4K image injection ({replaced_count} images) -> {PDF_PATH}")


def convert_docx_to_pdf():
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        doc = word.Documents.Open(DOCX_PATH)
        doc.Repaginate()
        for story in doc.StoryRanges:
            story.Fields.Update()
        doc.ExportAsFixedFormat(
            OutputFileName=PDF_PATH,
            ExportFormat=17,
            OpenAfterExport=False,
            OptimizeFor=0,
            CreateBookmarks=1,
        )
        doc.Close(SaveChanges=False)
        print(f"Exported base PDF via Microsoft Word: {PDF_PATH}")
    finally:
        word.Quit()

    inject_lossless_4k_images_into_pdf()


def render_pdf_pages_for_review():
    pdf_doc = fitz.open(PDF_PATH)
    num_pages = len(pdf_doc)
    print(f"Total PDF pages rendered: {num_pages}")

    for f in os.listdir(REVIEW_DIR):
        if f.endswith(".png"):
            os.remove(os.path.join(REVIEW_DIR, f))

    page_imgs = []
    for idx, page in enumerate(pdf_doc):
        pix = page.get_pixmap(dpi=300)
        out_png = os.path.join(REVIEW_DIR, f"page_{idx + 1}.png")
        pix.save(out_png)
        page_imgs.append(Image.open(out_png).convert("RGB"))
        print(f"  Rendered {out_png} ({pix.width}x{pix.height})")

    if page_imgs:
        thumb_w = 520
        thumb_h = int(page_imgs[0].size[1] * (thumb_w / page_imgs[0].size[0]))
        cols = 4
        rows = (len(page_imgs) + cols - 1) // cols
        pad = 24
        cs_w = cols * thumb_w + (cols + 1) * pad
        cs_h = rows * thumb_h + (rows + 1) * pad
        cs = Image.new("RGB", (cs_w, cs_h), "#E2E8F0")
        draw = ImageDraw.Draw(cs)
        for i, im in enumerate(page_imgs):
            r = i // cols
            c = i % cols
            x = pad + c * (thumb_w + pad)
            y = pad + r * (thumb_h + pad)
            im_t = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            cs.paste(im_t, (x, y))
            draw.rectangle((x - 2, y - 2, x + thumb_w + 2, y + thumb_h + 2), outline="#14263D", width=3)
        cs_path = os.path.join(REVIEW_DIR, "contact_sheet.png")
        cs.save(cs_path)
        print(f"Saved contact sheet: {cs_path}")

    pdf_doc.close()
    return num_pages


if __name__ == "__main__":
    build_docx()
    convert_docx_to_pdf()
    render_pdf_pages_for_review()
