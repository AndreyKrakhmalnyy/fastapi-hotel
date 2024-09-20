from hotels import router as router_hotels
from fastapi import FastAPI
import uvicorn


app = FastAPI()

app.include_router(router_hotels)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
