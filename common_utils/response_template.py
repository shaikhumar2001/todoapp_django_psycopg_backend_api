from django.http import JsonResponse
from datetime import datetime
from typing import Any

def response_template(success: bool=True, error_code: int=0, message: str="Success", data: Any=None, request: Any=None, status: int=200):
    """
    Standard API JSON response
    """
    return JsonResponse(
                {
                    "success": success,
                    "error_code": error_code,
                    "message": message or "",
                    "data": data or {},
                    "timestamp": datetime.now().isoformat(),
                    "path": request.path if request else None,
                },
                status=status
            )

