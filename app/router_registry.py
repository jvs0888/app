from pathlib import Path

try:
    from app.routers.index import index
    from app.routers.login import login
    from app.routers.dashboard import dashboard
except ImportError as ie:
    exit(f'{ie} :: {Path(__file__).resolve()}')


ROUTERS: list = [
    index,
    login,
    dashboard,
]
