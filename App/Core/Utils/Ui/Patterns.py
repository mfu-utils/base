class Patterns:
    DIRECTORY_WINDOWS = r'^\w:(\\[\w!-]+)*$'
    DIRECTORY_NON_WINDOWS = r'^(?:/[\w!-]+)+$'
    IP = r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$'
