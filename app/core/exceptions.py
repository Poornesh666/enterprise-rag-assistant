from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logging import logger


async def global_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected server errors.
    """

    logger.exception(f"Unexpected error: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error"
        },
    )