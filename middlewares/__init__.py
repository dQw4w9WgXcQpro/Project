from dispatcher import dp
from .user import UserMiddleware

if __name__ == 'middlewares':
    dp.setup_middleware(UserMiddleware())
