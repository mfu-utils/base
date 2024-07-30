import os
import pathlib
#: BUILD_TYPE:!server
import sys
#: END:BUILD_TYPE:!server
from os.path import dirname, abspath

ROOT = dirname(abspath(__file__))
HOME = pathlib.Path.home()
CWD = ROOT

if getattr(sys, 'frozen', False):
    CWD = os.path.dirname(sys.executable)


RCL_PROTOCOL_VERSION = 1

# Versions
VERSION_MAJOR = "@V_MAJOR@"
VERSION_MINOR = "@V_MINOR@"
VERSION_PATH = "@V_PATH@"
VERSION_BRANCH = "@V_BRANCH@"
VERSION_NUMBER = "@V_NUMBER@"
VERSION_SHOW = "@V_SHOW@"
VERSION_BUILD_DATE = "@V_BUILD_DATE@"
VERSION_DETAILED = f'{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATH} ({VERSION_NUMBER}) {VERSION_BRANCH}'

# StaticData
STATIC_APP_NAME = "@APP_NAME@"
STATIC_LICENSE_NAME = "@LICENSE_NAME@"
STATIC_LICENSE_URL = "@LICENSE_URL@"
STATIC_REPO_NAME = "@REPO_NAME@"
STATIC_REPO_URL = "@REPO_URL@"

# Settings files
ENV_NAME = '.env'
#: BUILD_TYPE:client-ui
INI_NAME = 'settings.ini'
#: END:BUILD_TYPE:client-ui

# Var paths
VAR = os.path.join(CWD, "var")
#: BUILD_TYPE:!server
# noinspection PyRedeclaration
if len(sys.argv) > 2 and sys.argv[1] == '--prefix-path':
    VAR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "var")
#: END:BUILD_TYPE:!server
ENV_PATH = os.path.join(VAR, ENV_NAME)
#: BUILD_TYPE:client-ui
INI_PATH = os.path.join(VAR, INI_NAME)
#: END:BUILD_TYPE:client-ui
CACHE_PATH = os.path.join(VAR, "cache")
SQLITE_PATH = os.path.join(VAR, "db")
LOGS_PATH = os.path.join(VAR, "logs")

# Configs parameters
CONFIGS_PATH = os.path.join(ROOT, "configs")

# Config files
CONFIG_FILES_METADATA = os.path.join(CONFIGS_PATH, "metadata.yml")
CONFIG_FILE_SERVICES = os.path.join(CONFIGS_PATH, "container.yml")

# Models
DB_MODELS_NAMESPACES = [
    # f"App.Models",
    #: BUILD_TYPE:client-ui
    f"App.Models.Client",
    #: END:BUILD_TYPE:client-ui
]

# Controllers paths
#: BUILD_TYPE:server
CONTROLLERS_NAMESPACES = {
    'App.Controllers',
}
#: END:BUILD_TYPE:server

# Console commands
COMMANDS_NAMESPACES = {
    'App.Commands',
    #: BUILD_TYPE:client-ui
    'App.Commands.Client',
    #: END:BUILD_TYPE:client-ui
}

# Assets paths
ASSETS = os.path.join(ROOT, "assets")

ICONS_PATH = os.path.join(ASSETS, "icons")
STYPES_PATH = os.path.join(ASSETS, "styles")
LANGS_DIR = os.path.join(ASSETS, "langs")
