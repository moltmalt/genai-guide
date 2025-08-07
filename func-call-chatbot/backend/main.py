from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from core.config import settings

from routers.tshirt import router as tshirt_router
from routers.cart import router as cart_router
from routers.order import router as order_router
from routers.chat import router as chat_router
from routers.auth import router as auth_router
from routers.wishlist import router as wishlist_router
from routers.middleware import (
    known_error_logger, 
    validation_error_logger, 
    http_exception_logger, 
    uncaught_exception_logger,
    KnownAppError
)

import uvicorn

app = FastAPI(
    title = "T-Shirt Store API",
    description="API for t-shirt ordering system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"   
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(tshirt_router, prefix="/api")
app.include_router(cart_router, prefix="/api")
app.include_router(order_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(wishlist_router, prefix="/api")

app.add_exception_handler(KnownAppError, known_error_logger)
app.add_exception_handler(RequestValidationError, validation_error_logger)
app.add_exception_handler(HTTPException, http_exception_logger)
app.add_exception_handler(Exception, uncaught_exception_logger)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  
        log_level="info"
    )
