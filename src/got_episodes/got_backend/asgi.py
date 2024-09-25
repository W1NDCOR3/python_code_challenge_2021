import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.wsgi import WSGIMiddleware
import httpx  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'got_backend.settings')

# Initialize Django ASGI application
django_asgi_app = get_asgi_application()

# Initialize FastAPI application
fastapi_app = FastAPI()

# CORS Middleware (if you need it)
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a FastAPI route for the root path
@fastapi_app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}

# Define a FastAPI route to proxy requests to OMDB API
@fastapi_app.get("/omdb")
async def get_omdb_data(i: str, apikey: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://www.omdbapi.com/?i={i}&apikey={apikey}")
        return response.json()  # Return the JSON response from the external API

# Mount the Django application to a specific path
fastapi_app.mount("/django", WSGIMiddleware(django_asgi_app))

# ASGI application entry point
application = fastapi_app
