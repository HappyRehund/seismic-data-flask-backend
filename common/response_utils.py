from flask import jsonify, Response
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
