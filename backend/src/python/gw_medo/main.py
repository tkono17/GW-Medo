from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .app import getApp
from .routers import (
    category_api,
    eventtype_api, 
    eventsession_api, 
    member_api, 
    topic_api, 
    file_api
)

app = FastAPI()
origins = [
    'http://localhost'
    'http://localhost:5173',
    '*'
]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

app.include_router(category_api.router)
app.include_router(member_api.router)
app.include_router(eventtype_api.router)
app.include_router(eventsession_api.router)
app.include_router(topic_api.router)
app.include_router(file_api.router)

gwmedo_app = getApp()
gwmedo_app.configFromEnv()
gwmedo_app.connectDb(gwmedo_app.settings.DBURL)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
