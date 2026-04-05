import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.getenv("MODEL_DIR", os.path.join(BASE_DIR, "models"))

ALLOWED_EXTENSIONS = os.getenv(
    "ALLOWED_EXTENSIONS",
    ".glb,.fbx"
).split(",")