from pypdf import PdfReader
import pypdfium2 as pdfium
from ocr import ocr_text
from PIL import Image
import os

def extract_text(file_path : str):
    fname = os.path.basename(file_path).lower()
    text = ""
    if fname.endswith(".pdf"):
        pdf = pdfium.PdfDocument(file_path)
        try:
            for i in range(len(pdf)):
                page = pdf.get_page(i)
                textpage = page.get_textpage()
                extracted_text = textpage.get_text_range()

                if extracted_text and extracted_text.strip() != "":
                    text += extracted_text + "\n\n"
                else:
                    image = page.render(scale=2).to_pil()
                    ocr_result = ocr_text(image)
                    if ocr_result:
                        text += ocr_result + "\n\n"

                page.close()
        finally:
            pdf.close()

        if not text or text.strip() == "":
            raise ValueError(f"No readable text extracted from {fname}")
        return text

    elif fname.endswith(".txt"):
        with open(file_path, "r", encoding= "utf-8", errors= "ignore") as f:
            text = f.read()
        return text
    elif fname.endswith((".jpg", ".jpeg", ".png", )):
        image = Image.open(file_path)
        text = ocr_text(image)
        return text
    else:
        raise ValueError(f"Unsupported file type: {fname}")

