import os
from app.config import MODEL_DIR, ALLOWED_EXTENSIONS


def generate_keyword_map():
    keyword_map = {}

    if not os.path.exists(MODEL_DIR):
        return keyword_map

    for file in os.listdir(MODEL_DIR):
        if any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            model_name = os.path.splitext(file)[0]

            words = model_name.lower().split("_")

            for word in words:
                if word not in keyword_map:
                    keyword_map[word] = set()

                keyword_map[word].add(model_name)

    # Convert set → list
    return {k: list(v) for k, v in keyword_map.items()}