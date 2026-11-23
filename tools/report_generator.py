from pathlib import Path
from datetime import datetime
import re
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)

def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return (slug[:55] or "research-report")

def save_report(topic: str, markdown: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"{_slug(topic)}_{stamp}"
    md_path = REPORT_DIR / f"{base}.md"
    docx_path = REPORT_DIR / f"{base}.docx"
    md_path.write_text(markdown, encoding="utf-8")

    doc = Document()
    for line in markdown.splitlines():
        line = line.rstrip()
        if not line:
            continue
        if line.startswith("# "):
            doc.add_heading(line[2:], level=1)
        elif line.startswith("## "):
            doc.add_heading(line[3:], level=2)
        elif line.startswith("### "):
            doc.add_heading(line[4:], level=3)
        elif line.startswith(("- ", "* ")):
            doc.add_paragraph(line[2:], style="List Bullet")
        elif len(line) > 2 and line[0].isdigit() and line[1:3] in (". ", ") "):
            doc.add_paragraph(line[3:], style="List Number")
        else:
            doc.add_paragraph(line)
    doc.save(docx_path)
    return str(md_path)
