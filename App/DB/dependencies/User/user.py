from uuid import UUID
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend
from App.DB.dependencies.User.usermanager import get_user_manager
from App.DB.model import User

#Using Bearer token to authentication the process
bearer_transport = BearerTransport(
    tokenUrl='auth/jwt/login'
)

#Using JWT to creating access token based on JSON
SECRET = 'SECRET'
def get_jwt_strategy():
    return JWTStrategy(
        secret=SECRET,
        lifetime_seconds=3600
)

#initiate the users authentication backend with all of the componen above
auth_backend = AuthenticationBackend(
    name='jwt',
    get_strategy=get_jwt_strategy,
    transport=bearer_transport
)

#the main fastapi users dependencies
fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)



