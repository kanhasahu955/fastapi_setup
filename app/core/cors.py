from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.env import get_settings


def setup_cors(app:FastAPI):
    settings = get_settings()
    origins = settings.cors_origins

    if isinstance(origins, str):
        origins = [o.strip() for o in origins.split(",")]

    app.add_middleware(CORSMiddleware,
                        allow_origins=origins,
                        allow_credentials=settings.cors_allow_credentials,
                        allow_methods=settings.cors_allow_methods,
                        allow_headers=settings.cors_allow_headers,
                        expose_headers=["Content-Disposition"],
                        max_age=600,
                    )
