from flask import jsonify, Response, make_response
from typing import Tuple
from dto.base import DtoResponse


def success_response(data: DtoResponse, status_code: int = 200) -> Tuple[Response, int]:
    """Build a standardized success JSON response"""
    return jsonify({
        "success": True,
        "data": dict(data.to_dict())
    }), status_code


def error_response(message: str, status_code: int = 400) -> Tuple[Response, int]:
    """Build a standardized error JSON response"""
    return jsonify({
        "success": False,
        "error": message
    }), status_code


def file_response(
    data: bytes,
    mime_type: str,
    filename: str,
    cache_max_age: int = 3600,
) -> Response:
    """Build a binary file response with proper headers.

    Best-practice headers for serving binary/image content:
    - Content-Type        → tells the browser how to interpret the bytes
    - Content-Length      → enables progress bars & range requests
    - Content-Disposition → inline (display) vs attachment (download)
    - Cache-Control       → allows client-side caching for static images
    - ETag (optional)     → enables conditional requests (304 Not Modified)
    """
    resp = make_response(data)
    resp.headers['Content-Type'] = mime_type
    resp.headers['Content-Length'] = len(data)
    resp.headers['Content-Disposition'] = f'inline; filename="{filename}"'
    resp.headers['Cache-Control'] = f'public, max-age={cache_max_age}'
    return resp
