from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.query_router import gemini_route_query  # ✅ Only import the Gemini router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query")
async def query_router(request: Request):
    data = await request.json()
    query = data.get("query", "")
    result = await gemini_route_query(query)  # ✅ Use Gemini-based router
    return result
