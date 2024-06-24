from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.jobs import lifespan
from api.routers.user import user_router
from api.routers.health import health_router
from api.routers.attachments import attachment_router
from api.routers.analyzer import analyzer_router
from api.routers.auth import magic_link_route

app = FastAPI(lifespan=lifespan)
app.include_router(attachment_router)
app.include_router(health_router)
app.include_router(user_router)
app.include_router(analyzer_router)
app.include_router(magic_link_route)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def run():
    import uvicorn

    uvicorn.run(__name__ + ":app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    run()
