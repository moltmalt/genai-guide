from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
import logging

class KnownAppError(Exception):
    """Custom exception for known application errors."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

async def known_error_logger(request: Request, exc: KnownAppError):
    logging.warning(f"Known error occurred: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )

async def validation_error_logger(request: Request, exc: RequestValidationError):
    logging.info(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

async def http_exception_logger(request: Request, exc: HTTPException):
    logging.error(f"HTTPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

async def uncaught_exception_logger(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred."},
    )