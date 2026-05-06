from fastapi import FastAPI, Depends
from .routers import category_api, member_api, event_api, topic_api, file_api
from .tools.common import get_query_token

app = FastAPI()

app.include_router(category_api.router)
app.include_router(member_api.router)
app.include_router(event_api.router)
app.include_router(topic_api.router)
app.include_router(file_api.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
