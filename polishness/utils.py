from os.path import abspath, dirname
from os import getenv


def get_project_dir():
    return abspath(dirname(dirname(__file__))) + '/'


PROJECT_DIR = get_project_dir()

if getenv("STATIC_PATH") is None:
    STATIC_DIR = f'{PROJECT_DIR}polishness/varlike/'
else:
    STATIC_DIR = getenv("STATIC_PATH")
