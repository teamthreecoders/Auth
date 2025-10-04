from typing import Any, List, Dict, Optional

def payload(
    success: bool,
    status_code:int,
    message: str,
    data: Optional[Any] = None,
    errors: Optional[List[Dict[str, str]]] = None,
    meta: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    
    return {
        "success": success,
        "status_code": status_code,
        "message": message,
        "data": data or {},
        "errors": errors or [],
        "meta": meta or {}
    }
