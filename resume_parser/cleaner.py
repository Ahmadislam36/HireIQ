import re

def clean_text(text):
    # Extra spaces hatao
    text = re.sub(r'\s+', ' ', text)
    # Special characters hatao
    text = re.sub(r'[^\w\s@.,|()/+-]', '', text)
    # Extra lines hatao
    text = text.strip()
    return text

def clean_resume_dict(resumes_dict):
    cleaned = {}
    for name, text in resumes_dict.items():
        cleaned[name] = clean_text(text)
    return cleaned

if __name__ == "__main__":
    from pdf_extractor import extract_text_from_pdf
    text = extract_text_from_pdf("data/uploads/Ahmad_Islam.pdf")
    cleaned = clean_text(text)
    print("✅ Cleaned Text:")
    print(cleaned[:500])