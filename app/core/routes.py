""""Routes приложения """
import typing

if typing.TYPE_CHECKING:
    from core.components import Application


def setup_routes(app: "Application"):
    """Настройка потключаемых route к приложению."""
    from auth.views import auth_route
    from convertor.views import convertor_route

    app.include_router(convertor_route)
    app.include_router(auth_route)
