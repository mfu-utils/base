from App.helpers import env


__CONFIG__ = {
    # Enable all debug info
    "debug": env("PRINTING_LIST_MODAL_DEBUG", False),

    # Check document what has been convert previously
    "check_previous": env("PRINTING_CHECK_PREVIOUS", True),
}

