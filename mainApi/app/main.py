from fastapi import (
    FastAPI, APIRouter,
)
from starlette.middleware.cors import CORSMiddleware

from mainApi.app.auth.routers import router as auth_router
from mainApi.app.db.mongodb_utils import connect_to_mongo, close_mongo_connection
# from mainApi.app.images.routers import router as image_router
from mainApi.config import ALLOWED_HOSTS

# from mainApi.config import connect_db, close_db

app = FastAPI(title='IAS Project')

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# ================= Routers  ===============
app.include_router(auth_router)
# app.include_router(image_router)

test_router = APIRouter(
    prefix="/test",
    tags=["test"]
)


@test_router.get("", response_description="Test endpoint, will return the request")
async def _test(request: str = None):
    if request:
        return request
    else:
        return "Pass any string as 'request' query parameter and it will return it. ex. /test/?request=foo"

app.include_router(test_router)
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
