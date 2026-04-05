from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from app.services.model_loader import generate_keyword_map
from app.services.ai_search import ai_match
from app.config import MODEL_DIR, ALLOWED_EXTENSIONS

app = FastAPI(
    title="3D Model API",
    description="AI-powered API for AR/3D chemistry models",
    version="2.0.0"
)

# ✅ CORS (for Flutter / Web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Always generate fresh keyword map
def get_keyword_map():
    return generate_keyword_map()


# ✅ Root
@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "AI 3D Model API running 🚀"
    }


# ✅ List all keywords
@app.get("/keywords")
async def list_keywords():
    keyword_map = get_keyword_map()
    return {
        "total_keywords": len(keyword_map),
        "keywords": list(keyword_map.keys())
    }


# ✅ 🔥 AI SEARCH ENDPOINT
@app.get("/search/{query}")
async def search_models(query: str):
    keyword_map = get_keyword_map()

    matched_keywords = ai_match(query, keyword_map)

    if not matched_keywords:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "no_match_found",
                "message": f"No match for '{query}'",
                "suggestions": list(keyword_map.keys())[:5]
            }
        )

    results = []
    all_models = set()

    # 🔥 collect models from ALL matched keywords
    for keyword in matched_keywords:
        models = keyword_map.get(keyword, [])
        for model in models:
            all_models.add(model)

    # 🔥 build response
    for model in all_models:
        for ext in ALLOWED_EXTENSIONS:
            filename = f"{model}{ext}"
            file_path = os.path.join(MODEL_DIR, filename)

            if os.path.exists(file_path):
                results.append({
                    "model_name": model,
                    "file": f"/download/{filename}"
                })

    return {
        "query": query,
        "matched_keywords": matched_keywords,
        "count": len(results),
        "models": results
    }


# ✅ Download model
@app.get("/download/{filename}")
async def download_model(filename: str):
    file_path = os.path.join(MODEL_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    ext = os.path.splitext(filename)[1]

    mime = (
        "model/gltf-binary"
        if ext == ".glb"
        else "application/octet-stream"
    )

    return FileResponse(
        file_path,
        media_type=mime,
        filename=filename
    )