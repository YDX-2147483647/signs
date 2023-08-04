from io import BytesIO
from pathlib import Path

from fpdf import FPDF
from pypdf import PdfReader, PdfWriter


def sign(doc: Path, signs: Path, out: Path) -> None:
    # fpdf2 can generate PDF groundless,
    # while pypdf can edit existing PDF.
    # https://pyfpdf.github.io/fpdf2/CombineWithPyPDF2.html

    # Convert signs to PDF
    signs_pdf = FPDF()
    signs_pdf.add_page()
    signs_pdf.image(signs, x=169, y=33, h=215)

    signs_page = PdfReader(BytesIO(signs_pdf.output())).pages[0]

    # Merge into the doc
    writer = PdfWriter(clone_from=doc)
    writer.pages[0].merge_page(signs_page)
    writer.write(out)


if __name__ == "__main__":
    doc = next(Path().glob("*.pdf"))
    out_dir = Path("out")
    signs = out_dir / "merged.png"
    doc_signed = out_dir / f"{doc.stem}-signed.pdf"

    sign(doc, signs, doc_signed)
