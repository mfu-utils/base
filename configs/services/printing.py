from App.helpers import env


__CONFIG__ = {
    # Enable all debug info
    "debug": env("PRINTING_LIST_MODAL_DEBUG", False),

    # Check document what has been convert previously
    "use_cached_docs": env("PRINTING_USE_CACHED_DOCUMENTS", False),

    # Save printer in cache for slow commands. Example: macOS local using.
    "use_cached_devices": env("PRINTING_USE_CACHED_DEVICES", False),
}

