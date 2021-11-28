from fastapi import (
    FastAPI,
)
from mainApi.auth.routers import router as auth_router
from mainApi.images.routers import router as image_router
# from mainApi.config import connect_db, close_db

app = FastAPI()

# app.add_event_handler("startup", connect_db)
# app.add_event_handler("shutdown", close_db)

# ================= Routers  ===============
app.include_router(auth_router)
app.include_router(image_router)
#
# # ================ Authentication Middleware =======================
# #----------- Here authentication is based on basic scheme,
# #----------- another authentication, based on bearer scheme, is used throughout
# #---------- the application (as decribed in FastAPI official documentation)
# @app.middleware("http")
# async def authenticate(request: Request, call_next):
#
# #-------------------- Authentication basic scheme -----------------------------
#     if "Authorization" in request.headers:
#         auth = request.headers["Authorization"]
#         try:
#             scheme, credentials = auth.split()
#             if scheme.lower() == 'basic':
#                 decoded = base64.b64decode(credentials).decode("ascii")
#                 username, _, password = decoded.partition(":")
#                 request.state.user = await authenticate_user(username, password)
#         except (ValueError, UnicodeDecodeError, binascii.Error):
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid basic auth credentials"
#             )
#
#     response = await call_next(request)
#     return response
