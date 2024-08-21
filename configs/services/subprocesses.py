from App.helpers import env

__CONFIG__ = {
    'debug': env('SUBPROCESSES_DEBUG', False),

    # host, wsl
    'linux_target_commands': env('LINUX_TARGET_COMMANDS', 'host'),
}
