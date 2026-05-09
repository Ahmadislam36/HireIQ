import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY", "")
UPLOAD_FOLDER   = "data/uploads/"
FAISS_FOLDER    = "data/faiss_index/"
REPORT_FOLDER   = "data/reports/"