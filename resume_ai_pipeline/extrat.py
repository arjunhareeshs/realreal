#!/usr/bin/env python3
"""
extrat.py
CLI test harness for extractors.extract_text_auto — supports PDF, DOCX, PNG, JPG
"""

import argparse
import logging
import sys
import os
# Import new PaddleOCR functions instead of the old ones
from extractors import extract_text_auto, extract_text_from_scanned_pdf, extract_text_from_image, clean_text
# from PIL import Image # No longer strictly needed here, but can stay
# import pytesseract # REMOVE pytesseract

LOG = logging.getLogger("extrat")

def setup_logging(level=logging.INFO):
    fmt = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=level, format=fmt)

def main():
    parser = argparse.ArgumentParser(description="Test resume text extraction (PDF/DOCX/Image)")
    parser.add_argument("path", help="Path to input file (.pdf, .docx, .png, .jpg)")
    parser.add_argument("--ocr", action="store_true", help="Force OCR path for images or PDFs")
    parser.add_argument("--out", "-o", help="Save extracted text to output file")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    setup_logging(logging.DEBUG if args.debug else logging.INFO)

    path = args.path
    if not os.path.exists(path):
        LOG.error("File not found: %s", path)
        sys.exit(2)

    try:
        LOG.info("Extracting from: %s", path)
        ext = os.path.splitext(path)[1].lower()

        # ---------- CASE 1: OCR forced ----------
        if args.ocr:
            if ext == ".pdf":
                # Now uses PaddleOCR (extract_text_from_scanned_pdf is updated)
                text = extract_text_from_scanned_pdf(path) 
            elif ext in [".png", ".jpg", ".jpeg"]:
                # Now uses PaddleOCR (extract_text_from_image is new)
                text = extract_text_from_image(path) 
            else:
                LOG.warning("OCR forced but file type %s not supported. Using auto.", ext)
                text = extract_text_auto(path)
        # ---------- CASE 2: automatic ----------
        else:
            # extract_text_auto handles all the logic internally now
            text = extract_text_auto(path)

        if not text.strip():
            LOG.warning("⚠️ No text extracted. Try --ocr mode or higher DPI.")
        else:
            LOG.info("✅ Extracted %d characters (%d words)", len(text), len(text.split()))

        # ---------- OUTPUT ----------
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(text)
            LOG.info("Saved extracted text to: %s", args.out)
        else:
            print("\n--- EXTRACTED TEXT START ---\n")
            print(text[:2000])  # show first part
            print("\n--- EXTRACTED TEXT END ---\n")

    except Exception as e:
        LOG.exception("❌ Extraction failed: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()