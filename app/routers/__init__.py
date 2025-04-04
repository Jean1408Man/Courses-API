from .auth import router as auth_router
from .users import router as users_router
from .courses import router as courses_router

all_routers = [
    auth_router,
    users_router,
    courses_router
]

