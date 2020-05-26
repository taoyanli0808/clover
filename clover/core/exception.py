
class CloverException(Exception): pass

class DatabaseException(CloverException): pass

class PythonException(CloverException): pass

class RequestException(CloverException): pass

class ResponseException(CloverException): pass