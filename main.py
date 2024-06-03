from fastapi import FastAPI

# Import your app configuration (replace with your actual file)
from config import settings

# Import your API routers (replace with your actual module names)
from api.auth import auth_endpoints
from api.orders import orders_endpoints
from api.products import products_endpoints

# Create the FastAPI application instance
app = FastAPI(title=settings.app_title, description=settings.app_description)

# Include API routers
app.include_router(auth_endpoints.router)
app.include_router(orders_endpoints.router)
app.include_router(products_endpoints.router)

# You can add additional application logic here if needed

# Main function for running the application (optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
