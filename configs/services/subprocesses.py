from App.helpers import env

__CONFIG__ = {
    'debug': env('SUBPROCESSES_DEBUG', False),
}
