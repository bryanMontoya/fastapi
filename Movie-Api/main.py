import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Mi Movie App"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind = engine)

@app.get('/', tags = ['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

#if __name__ == "__main__":
#    uvicorn.run("main:app", port = 5000, log_level = "info", reload = True)