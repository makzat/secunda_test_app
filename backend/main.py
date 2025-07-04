import logging

import uvicorn
from pythonjsonlogger import json

from backend.app import create_app
from backend.config import get_settings
from backend.routers import organization_router

settings = get_settings()

main_app = create_app()
main_app.include_router(organization_router)

handler = logging.StreamHandler()
handler.setFormatter(
    fmt=json.JsonFormatter("%(asctime)s 	%(levelname)s %(module)s %(message)s", json_ensure_ascii=False)
)
logging.basicConfig(level=logging.INFO, handlers=(handler,))

if __name__ == "__main__":
    uvicorn.run(app="main:main_app", host=settings.run.host, port=settings.run.port, reload=True)
