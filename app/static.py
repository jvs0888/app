import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles

directory: str = os.path.join(Path(__file__).parent.parent, 'static')

static_files: dict = {
    'path': '/static',
    'app': StaticFiles(directory=directory),
    'name': 'static'
}