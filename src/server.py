"""
Standard microservice API router boilerplate.
"""
from typing import Dict, Any
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MicroserviceApp:
    def __init__(self, service_name: str = "luke-service"):
        self.service_name = service_name
        self.routes: Dict[str, Any] = {}

    def route(self, path: str):
        def decorator(handler):
            self.routes[path] = handler
            return handler
        return decorator

    def handle_request(self, path: str, method: str = "GET") -> Dict[str, Any]:
        if path == "/health":
            return {"status": "UP", "service": self.service_name, "version": "1.0.0"}
        
        handler = self.routes.get(path)
        if not handler:
            return {"error": "Not Found", "code": 404}
            
        try:
            return {"data": handler(), "code": 200}
        except Exception as err:
            logger.error(f"Handler error for {path}: {err}")
            return {"error": "Internal Server Error", "code": 500}

app = MicroserviceApp()

@app.route("/api/v1/ping")
def ping_handler():
    return {"message": "pong"}
