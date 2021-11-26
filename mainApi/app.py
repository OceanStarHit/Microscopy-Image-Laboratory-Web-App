import base64
import binascii
import subprocess

import uvicorn
from fastapi import (
    FastAPI,
    HTTPException,
    status,
    Request,
)
from fastapi.security import OAuth2PasswordBearer
from mainApi.auth.routers import router as auth_router
from mainApi.auth.routers_b import router as auth_router_b
from mainApi.auth.auth import authenticate_user
# from mainApi.config import connect_db, close_db
from mainApi.models.user import UserModel

app = FastAPI()

# app.add_event_handler("startup", connect_db)
# app.add_event_handler("shutdown", close_db)

# ================= Routers  ===============
app.include_router(auth_router)
app.include_router(auth_router_b)

# ================ Authentication Middleware =======================
#----------- Here authentication is based on basic scheme,
#----------- another authentication, based on bearer scheme, is used throughout
#---------- the application (as decribed in FastAPI official documentation)
@app.middleware("http")
async def authenticate(request: Request, call_next):

#-------------------- Authentication basic scheme -----------------------------
    if "Authorization" in request.headers:
        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() == 'basic':
                decoded = base64.b64decode(credentials).decode("ascii")
                username, _, password = decoded.partition(":")
                request.state.user = await authenticate_user(username, password)
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid basic auth credentials"
            )

    response = await call_next(request)
    return response

#
# @app.get("/", tags=["Root"])
# async def read_root():
#     return {"message": "Welcome to this fantastic app."}

# if __name__ == "__main__":
#     print(f"__name__ ===== {__name__}")
#     # from mainApi import app as _app
#     # subprocess.call(["sh", "./mainApi/start.sh"])
#     print("mainApi.app:app")
#     uvicorn.run("mainApi.app:app", host="0.0.0.0", port=8000)