import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_all_resumes(upload_folder):
    resumes = {}
    for filename in os.listdir(upload_folder):
        if filename.endswith(".pdf"):
            full_path = os.path.join(upload_folder, filename)
            name = filename.replace(".pdf", "")
            resumes[name] = extract_text_from_pdf(full_path)
            print(f"✅ Extracted: {filename}")
    return resumes

if __name__ == "__main__":
    # apni PDF ka naam yahan likho
    text = extract_text_from_pdf("data/uploads/Ahmad_Islam.pdf")
    print(text)