import fitz
from pdf2image import convert_from_path
# import pytesseract # REMOVE pytesseract
from PIL import Image
from docx import Document
import re, os
from paddleocr import PaddleOCR # IMPORT PaddleOCR

# Initialize PaddleOCR globally or within the function for efficiency
# Use_gpu=False is recommended unless you have a properly configured GPU
# lang='en' specifies the English language model
PADDLE_OCR = PaddleOCR(use_angle_cls=True, lang='en')
def clean_text(t: str) -> str:
    t = re.sub(r'\r\n|\r', '\n', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()

def extract_text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    pages = [page.get_text("text") for page in doc]
    return clean_text("\n\n".join(pages))

def extract_text_from_scanned_pdf(path: str, dpi=300) -> str:
    """Uses PaddleOCR for scanned PDFs"""
    pages = convert_from_path(path, dpi=dpi)
    text = []
    for img in pages:
        # Save image to a temp file path for PaddleOCR
        temp_path = "temp_page.png" 
        img.save(temp_path)
        
        # Run PaddleOCR
        result = PADDLE_OCR.ocr(temp_path, cls=True)
        # Extract text from the result structure
        page_text = "\n".join([line[1][0] for line in result[0]])
        text.append(page_text)
        os.remove(temp_path)

    return clean_text("\n\n".join(text))

def extract_text_from_image(path: str) -> str:
    """Uses PaddleOCR for image files"""
    result = PADDLE_OCR.ocr(path, cls=True)
    # The result is a list of lists; the actual text is in result[0]
    # We join all extracted lines
    text = "\n".join([line[1][0] for line in result[0]])
    return clean_text(text)

def extract_text_from_docx(path: str) -> str:
    doc = Document(path)
    paras = [p.text for p in doc.paragraphs if p.text.strip()]
    return clean_text("\n\n".join(paras))

def extract_text_auto(path: str, scanned_ocr_threshold=50) -> str:
    ext = os.path.splitext(path)[1].lower()
    
    if ext == ".pdf":
        txt = extract_text_from_pdf(path)
        # Use OCR if the plain text extraction yields very little text
        if len(txt.split()) < scanned_ocr_threshold:
            print("⚠️ Low text count detected. Switching to PaddleOCR for PDF.")
            txt = extract_text_from_scanned_pdf(path)
        return txt
        
    elif ext == ".docx":
        return extract_text_from_docx(path)
        
    elif ext in [".png", ".jpg", ".jpeg"]:
        # Use new PaddleOCR function for images
        return extract_text_from_image(path)
        
    else:
        raise ValueError(f"Unsupported file type {ext}")