import uvicorn
from asyncio import get_event_loop

from fastapi import FastAPI

from config import settings
from routers.user import router as user_router


app = FastAPI()
app.include_router(user_router)

# if __name__ == "__main__":
#     loop = get_event_loop()
#     config = uvicorn.Config(app=app, port=settings.SERVER_PORT, loop=loop)
#     server = uvicorn.Server(config)
#     loop.run_until_complete(server.serve())
