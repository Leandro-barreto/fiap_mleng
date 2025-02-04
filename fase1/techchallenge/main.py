from fastapi import FastAPI
from routers import localdata, webdata

app = FastAPI()

app.include_router(localdata.router)
app.include_router(webdata.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the WINE API"}
