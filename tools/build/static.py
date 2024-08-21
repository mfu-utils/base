from App.helpers import platform
from config import ROOT
import os

"""
Build types specific blocks:
    '#: BUILD_TYPE:<type>' - Start building type block
    '#: END:BUILD_TYPE:<type>' - End building type block

Platform specific blocks:
    '#: PLATFORM:<name>' - Start building platform block
    '#: END:PLATFORM:<name>' - End building platform block

Delete blocks:
    '#: DELETE' - Start delete block
    '#: END:DELETE' - End delete block
"""

STRUCT_FILE_NAME = "struct.json"
PARAMETERS_FILE_NAME = "parameters.json"

BUILD_LOGS_DIR = '.build_logs'

BUILD_DIRECTORY = str(os.path.join(ROOT, "build"))

BUILD_TYPE_SERVER = 'server'
BUILD_TYPE_CLIENT = 'client'
BUILD_TYPE_CLIENT_UI = 'client-ui'

PLATFORM_BUILD_TYPES = {
    BUILD_TYPE_SERVER,
    BUILD_TYPE_CLIENT,
    BUILD_TYPE_CLIENT_UI,
}

AVAILABLE_PLATFORM_BUILD_TYPES = {
    'Windows': [
        # BUILD_TYPE_CLIENT,
        BUILD_TYPE_CLIENT_UI,
        # BUILD_TYPE_ENDPOINT_PORTABLE_CLIENT_UI,
    ],
    'Linux': [
        BUILD_TYPE_SERVER,
        # BUILD_TYPE_CLIENT,
        # BUILD_TYPE_CLIENT_UI,
        # BUILD_TYPE_ENDPOINT_PORTABLE_CLIENT_UI,
    ],
    'Darwin': [
        # BUILD_TYPE_SERVER
        # BUILD_TYPE_CLIENT,
        # BUILD_TYPE_CLIENT_UI,
        # BUILD_TYPE_ENDPOINT_PORTABLE_CLIENT_UI,
    ]
}

REMOVE_AFTER_BUILD = {
    '_': {},
    'build-types': {
        BUILD_TYPE_SERVER: {},
        BUILD_TYPE_CLIENT: {},
        BUILD_TYPE_CLIENT_UI: {},
        # BUILD_TYPE_ENDPOINT_PORTABLE_CLIENT_UI: {}
    },
    'platforms': {
        'Windows': {},
        'Linux': {},
        'Darwin': {},
    },
}

DISABLED_UI = {
    # End points
    "client-ui": ROOT,

    # Assets
    "assets": ROOT,
    "logo.ico": ROOT,

    # App code
    "Ui": [os.path.join(ROOT, "App", "Core"), os.path.join(ROOT, "App", "Core", "Utils")],
    "Widgets": [os.path.join(ROOT, "App", "Core"), os.path.join(ROOT, "App")],
    "Langs": os.path.join(ROOT, "App", "Core"),

    # Services
    "ui.py": os.path.join(ROOT, "configs", "services"),
    "ocr_convertor.py": os.path.join(ROOT, "configs", "services"),
    "langs.py": os.path.join(ROOT, "configs", "services"),
    "notification.py": os.path.join(ROOT, "configs", "services"),

    # UI configs
    "ui": os.path.join(ROOT, "configs"),
}

DISABLED_CLIENT = {
    # End points
    "client": ROOT,

    # App code
    "Client": [
        os.path.join(ROOT, "App", "Core", "Network"),
        os.path.join(ROOT, "App", "Models"),
        os.path.join(ROOT, "App", "Services"),
        os.path.join(ROOT, "db", "seeders"),
        os.path.join(ROOT, "App", "Commands"),
        os.path.join(ROOT, "App", "Core", "Utils"),
    ],

    # Configs
    "client.py": os.path.join(ROOT, "configs", "services"),

    # Static
    "console.bat": os.path.join(ROOT, "console.bat"),

    **DISABLED_UI
}

DISABLED_SERVER = {
    # Endpoints
    "server": ROOT,

    # App code
    "Controllers": os.path.join(ROOT, "App"),
    "Server": [
        os.path.join(ROOT, "App", "Core", "Network"),
    ],
    "Handlers": os.path.join(ROOT, "App", "Core", "Network"),
    "AbstractReceiveDataHandler.py": os.path.join(ROOT, "App", "Core", "Abstract"),
    "AbstractConnectionHandler.py": os.path.join(ROOT, "App", "Core", "Abstract"),
    "RedisCacheDriver.py": os.path.join(ROOT, "App", "Core", "Cache"),
}

DISABLED_BUILD_ITEMS = {
    # In all platforms and build types
    '_': {
        ".idea": "*",
        ".vscode": "*",
        ".fleet": "*",
        ".git": "*",
        "__pycache__": "*",
        ".gitignore": "*",
        ".DS_Store": "*",
        "tools": ROOT,
        "ci": ROOT,
        "ci.yaml": ROOT,
        "ci.yaml.example": ROOT,
        "README.md": ROOT,
        "build": ROOT,
        ".venv": ROOT,
        "envs": ROOT,
        "docs": ROOT,
        "tmp": ROOT,
        "var": ROOT,
        "Makefile": ROOT,
    },
    # Platforms specific
    "platforms": {
        "Linux": {
            "console.bat": ROOT,
        },
        "Windows": {
            #
        },
        "Darwin": {
            "console.bat": ROOT,
        }
    },
    # Build type specific
    "build-types": {
        BUILD_TYPE_SERVER: DISABLED_CLIENT,
        BUILD_TYPE_CLIENT: {**DISABLED_SERVER, **DISABLED_UI},
        BUILD_TYPE_CLIENT_UI: DISABLED_SERVER,
        # BUILD_TYPE_ENDPOINT_PORTABLE_CLIENT_UI: {}
    }
}

BUILD_PLATFORMS = [
    platform().DARWIN,
    platform().WINDOWS,
    platform().LINUX,
]

BUILD_TYPES = [
    BUILD_TYPE_SERVER,
    BUILD_TYPE_CLIENT,
    BUILD_TYPE_CLIENT_UI,
]

FILTERED_FILES_EXT = ['py', 'yml', 'yaml', 'txt']
