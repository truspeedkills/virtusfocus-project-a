"""
Build per-segment combined print packets and a printer instructions sheet.

Outputs (all in Focus Group Materials/Print Packets/):
  - Institutional_Packet.pdf   (worksheet + artifact cover + 9 artifacts)
  - D2C_Athlete_Packet.pdf     (worksheet + artifact cover + 11 artifacts)
  - GTM_Packet.pdf             (worksheet + artifact cover + 13 artifacts)
  - Printer_Instructions.txt + .docx + .pdf  (standalone vendor handoff sheet)

Assembly order per packet:
  1. Worksheet (segment-specific, used during Q1-Q5 of the breakout)
  2. Artifact Packet Cover (1-2 pages, segment-colored cover stock)
  3. Artifact contents in the order listed on that cover

Re-runnable: regenerates from latest individual PDFs in Focus Group Materials/.
After any single artifact PDF gets regenerated (e.g. after Word formatting
tweaks rendered via convert_one), re-run this script to refresh the combined
packets.

Run from project root:
    python scripts/build_print_packets.py
"""

import os
import sys
from pathlib import Path
from pypdf import PdfWriter, PdfReader

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE = REPO_ROOT / "Focus Group Materials"
OUT_DIR = BASE / "Print Packets"


# ---------------------------------------------------------------------------
# Per-segment assembly (worksheet first, artifact cover, then artifacts in
# cover-listed order).
# ---------------------------------------------------------------------------

SEGMENTS = {
    "Institutional_Packet.pdf": {
        "label": "Institutional",
        "color": "Deep blue (corporate / institutional tone)",
        "quantity": 6,
        "files": [
            BASE / "Worksheets" / "Institutional_Worksheet.pdf",
            BASE / "Artifact Packets" / "Institutional_Cover.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_Athlete_Snapshot.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_12-Week_Progression_Visual.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_2026-03-09to2026-03-15_VF_WeeklyInsight.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_2026-04-20to2026-04-26_VF_WeeklyInsight.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_2026-04-20to2026-04-26_VF_CoachingMessage.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_2026-04-20to2026-04-26_VF_ParentMessage.pdf",
            BASE / "Athlete Materials" / "Angelo Allen" / "Angelo_Allen_10-Week_Progression_Visual.pdf",
            BASE / "Athlete Materials" / "Angelo Allen" / "Angelo_Allen_2026-04-20to2026-04-26_VF_WeeklyInsight.pdf",
            BASE / "Sample Team Snapshot" / "Sample_Team_Snapshot.pdf",
        ],
    },
    "D2C_Athlete_Packet.pdf": {
        "label": "D2C / Athlete",
        "color": "Forest green (athletic / growth tone)",
        "quantity": 4,
        "files": [
            BASE / "Worksheets" / "D2C_Athlete_Worksheet.pdf",
            BASE / "Artifact Packets" / "D2C_Athlete_Cover.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_Athlete_Snapshot.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_12-Week_Progression_Visual.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_2026-03-09to2026-03-15_VF_CoachingMessage.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_2026-04-20to2026-04-26_VF_CoachingMessage.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_2026-04-20to2026-04-26_VF_DeepDive.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_2026-04-20to2026-04-26_VF_WeeklyInsight.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_2026-04-20to2026-04-26_VF_ParentMessage.pdf",
            BASE / "Athlete Materials" / "Angelo Allen" / "Angelo_Allen_10-Week_Progression_Visual.pdf",
            BASE / "Athlete Materials" / "Angelo Allen" / "Angelo_Allen_2026-04-20to2026-04-26_VF_CoachingMessage.pdf",
            BASE / "Athlete Materials" / "Hunter Snyder" / "Hunter_Snyder_2026-04-20to2026-04-26_VF_ParentMessage.pdf",
            BASE / "Sample Team Snapshot" / "Sample_Team_Snapshot.pdf",
        ],
    },
    "GTM_Packet.pdf": {
        "label": "GTM",
        "color": "Amber / burnt orange (strategy / commerce tone)",
        "quantity": 4,
        "files": [
            BASE / "Worksheets" / "GTM_Worksheet.pdf",
            BASE / "Artifact Packets" / "GTM_Cover.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_Athlete_Snapshot.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_12-Week_Progression_Visual.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_2026-04-20to2026-04-26_VF_CoachingMessage.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_2026-04-20to2026-04-26_VF_WeeklyInsight.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_2026-04-20to2026-04-26_VF_ParentMessage.pdf",
            BASE / "Athlete Materials" / "Grace Kindel" / "Grace_Kindel_2026-04-20to2026-04-26_VF_ParentInsight.pdf",
            BASE / "Athlete Materials" / "Angelo Allen" / "Angelo_Allen_Athlete_Snapshot.pdf",
            BASE / "Athlete Materials" / "Angelo Allen" / "Angelo_Allen_10-Week_Progression_Visual.pdf",
            BASE / "Athlete Materials" / "Angelo Allen" / "Angelo_Allen_2026-04-20to2026-04-26_VF_CoachingMessage.pdf",
            BASE / "Athlete Materials" / "Hunter Snyder" / "Hunter_Snyder_Athlete_Snapshot.pdf",
            BASE / "Athlete Materials" / "Hunter Snyder" / "Hunter_Snyder_2026-04-20to2026-04-26_VF_ParentMessage.pdf",
            BASE / "Sample Team Snapshot" / "Sample_Team_Snapshot.pdf",
            BASE / "Artifact Packets" / "Selected_App_Mockup_Printouts.pdf",
        ],
    },
}


def merge_pdfs(files, output_path):
    """Concatenate PDFs in order. Preserves vector quality (no re-render)."""
    writer = PdfWriter()
    for f in files:
        if not f.exists():
            raise RuntimeError(f"Missing source PDF: {f}")
        reader = PdfReader(str(f))
        for page in reader.pages:
            writer.add_page(page)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as fp:
        writer.write(fp)
    return len(writer.pages)


def page_count(pdf_path):
    return len(PdfReader(str(pdf_path)).pages)


def build_combined_packets():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    page_counts = {}
    for name, info in SEGMENTS.items():
        out = OUT_DIR / name
        pages = merge_pdfs(info["files"], out)
        page_counts[name] = pages
        print(f"  {name:<28} {pages:>3} pages from {len(info['files'])} sources")
    return page_counts


def cover_stock_pages_for(name, page_counts):
    """
    Worksheet is always 7 pages. Artifact packet cover comes immediately after.
    Returns the page range string for the printer instructions.
    """
    worksheet_pages = page_count(SEGMENTS[name]["files"][0])
    cover_pages = page_count(SEGMENTS[name]["files"][1])
    start = worksheet_pages + 1
    end = worksheet_pages + cover_pages
    if cover_pages == 1:
        return f"Page {start} (1 page on segment-colored cover stock)"
    return f"Pages {start}-{end} ({cover_pages} pages on segment-colored cover stock)"


def build_printer_instructions(page_counts):
    """Write Printer_Instructions.txt and convert to .docx + .pdf via convert_one()."""
    total_packets = sum(info["quantity"] for info in SEGMENTS.values())
    total_pages = sum(page_counts[name] * SEGMENTS[name]["quantity"] for name in SEGMENTS)

    lines = []
    lines.append('PRINTER INSTRUCTIONS')
    lines.append('"VirtusFocus" Focus Group, May 9, 2026')
    lines.append('=' * 60)
    lines.append('')
    lines.append('OVERVIEW')
    lines.append('')
    lines.append(f'Three PDF files, one per attendee segment, in this folder.')
    lines.append(f'Total print run: {total_packets} attendee packets, {total_pages} total pages.')
    lines.append('')
    lines.append('Each segment has its own segment color (deep blue, forest green,')
    lines.append('amber) used on the artifact packet cover page to enable visual')
    lines.append('sorting during the focus group breakout.')
    lines.append('')
    lines.append('')

    for name, info in SEGMENTS.items():
        pages = page_counts[name]
        cover_range = cover_stock_pages_for(name, page_counts)

        lines.append(f'== {info["label"].upper()} PACKET ==')
        lines.append('')
        lines.append(f'File:                {name}')
        lines.append(f'Total pages:         {pages}')
        lines.append(f'Quantity needed:     {info["quantity"]} copies')
        lines.append(f'Cover stock pages:   {cover_range}')
        lines.append(f'Cover stock color:   {info["color"]}')
        lines.append(f'Cover stock weight:  60-80 lb')
        lines.append(f'Body paper:          Standard 20-24 lb white')
        lines.append(f'Color printing:      Required for entire packet')
        lines.append(f'Binding:             Stapled top-left corner OR paperclip')
        lines.append('')
        lines.append('')

    lines.append('NOTES ON COVER STOCK')
    lines.append('')
    lines.append('Cover stock pages are the artifact packet cover pages within')
    lines.append('each combined packet. They are intended to print on segment-')
    lines.append('colored cover stock to provide a visual divider between the')
    lines.append('worksheet and the artifact contents, and to support at-a-')
    lines.append('glance segment sorting during the breakout transition.')
    lines.append('')
    lines.append('Worksheet pages (pages 1 through 7 of each packet) print on')
    lines.append('standard white paper. The worksheet design has segment-colored')
    lines.append('header bands baked into the layout, so colored paper stock is')
    lines.append('not required for those pages.')
    lines.append('')
    lines.append('All artifact pages after the cover (athlete snapshots, coaching')
    lines.append('messages, deep dives, coach insights, parent materials, team')
    lines.append('snapshot, mockup printouts) print on standard white paper.')
    lines.append('')
    lines.append('')
    lines.append('COLOR REQUIREMENTS')
    lines.append('')
    lines.append('Color printing is required for the entire packet. Several pages')
    lines.append('contain colored elements that lose meaning if printed in')
    lines.append('grayscale: gradient progression bars on the athlete progression')
    lines.append('visuals, amber-bordered callout boxes on coaching message')
    lines.append('cards, traffic-light color bands on the team snapshot, and')
    lines.append('header bands on every worksheet page. Standard CMYK four-')
    lines.append('color process is sufficient.')
    lines.append('')
    lines.append('')
    lines.append('CONFIDENTIALITY')
    lines.append('')
    lines.append('All material is confidential under NDA. Please do not retain')
    lines.append('digital file copies or sample prints after delivery. Contact')
    lines.append('Arron Beckes if any pages render unclearly or any colored')
    lines.append('elements look off before running the full print job.')
    lines.append('')

    txt_path = OUT_DIR / "Printer_Instructions.txt"
    txt_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Wrote: {txt_path.relative_to(REPO_ROOT)}")

    # Render .docx + .pdf via project's existing convert_one helper.
    sys.path.insert(0, str(REPO_ROOT))
    from make_reference_docs import convert_one  # noqa: E402
    convert_one(str(txt_path))


def main():
    print("Building combined print packets")
    print("-" * 60)
    page_counts = build_combined_packets()
    print()
    print("Building printer instructions sheet")
    print("-" * 60)
    build_printer_instructions(page_counts)
    print()
    print("Done. Outputs in:", OUT_DIR.relative_to(REPO_ROOT))


if __name__ == "__main__":
    main()
