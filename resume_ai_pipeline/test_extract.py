# test_extract.py
from extractors import extract_text_auto
import sys, os

def pretty_print_head(text, n=800):
    print("="*20)
    print("OUTPUT (first {} chars)".format(n))
    print("="*20)
    print(text[:n])
    print("\n\nTotal words:", len(text.split()))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_extract.py /path/to/resume.pdf")
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.exists(path):
        print("File not found:", path); sys.exit(1)
    txt = extract_text_auto(path)
    pretty_print_head(txt)
