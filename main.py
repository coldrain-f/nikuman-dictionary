import sqlite3
from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="JAKO Dict API")

BASE_DIR = Path(__file__).parent
RESOURCES_DIR = BASE_DIR / "resources"

# --- Database helpers ---

DB_PATHS = {
    "jako": RESOURCES_DIR / "Ja-Ko_DIC_2018.sqlite",
    "hanja": RESOURCES_DIR / "Hanja-Ko_DIC_2018.sqlite",
}

TABLE_NAMES = {
    "jako": "Ja_Ko_DIC_2018",
    "hanja": "Hanja_Ko_DIC_2018",
}


def get_connection(dict_type: str) -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATHS[dict_type]))
    conn.row_factory = sqlite3.Row
    return conn


# --- API endpoints ---

@app.get("/api/search")
def search(
    q: str = Query(..., min_length=1, description="검색어"),
    dict: str = Query("jako", pattern="^(jako|hanja)$", description="사전 종류"),
    limit: int = Query(20, ge=1, le=100, description="최대 결과 수"),
):
    """
    단어 검색 API.
    - 정확 매칭 결과를 우선 반환하고, 부분 매칭(전방 일치)을 추가로 반환합니다.
    """
    conn = get_connection(dict)
    table = TABLE_NAMES[dict]

    try:
        # 1) 정확 매칭
        exact = conn.execute(
            f"SELECT word, definition FROM [{table}] WHERE word = ? ORDER BY id ASC LIMIT ?",
            (q, limit),
        ).fetchall()

        results = [{"word": row["word"], "definition": row["definition"]} for row in exact]

        # 2) 부분 매칭 (전방 일치) — 정확 매칭으로 부족할 때
        if len(results) < limit:
            remaining = limit - len(results)
            partial = conn.execute(
                f"SELECT word, definition FROM [{table}] WHERE word LIKE ? AND word != ? ORDER BY id ASC LIMIT ?",
                (f"{q}%", q, remaining),
            ).fetchall()
            results.extend(
                {"word": row["word"], "definition": row["definition"]} for row in partial
            )

        return {"query": q, "dict": dict, "count": len(results), "results": results}
    finally:
        conn.close()


# --- Static files ---

# index.html을 루트에서 서빙
@app.get("/")
def serve_index():
    return FileResponse(str(BASE_DIR / "index.html"))


# 폰트 및 기타 정적 파일
app.mount("/", StaticFiles(directory=str(BASE_DIR)), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
