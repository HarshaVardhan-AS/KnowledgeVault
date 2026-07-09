from fastapi import UploadFile, HTTPException, status
from pypdf import PdfReader

def extract_text(file : UploadFile):
    fname = file.filename.lower()
    if fname.endswith(".pdf"):
        reader = PdfReader(file.file)
        pages = reader.pages
        text = ""
        for page in pages:
            extracted_text = page.extract_text()
            if extracted_text is not None:
                text+= extracted_text
        if text == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PDF is empty")
        return text

    elif fname.endswith(".txt"):
        text = file.file.read()
        text = text.decode("utf-8")
        return text
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type")

