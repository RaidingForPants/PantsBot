import environment

_logger = None

def get_instance():
    global _logger
    if _logger == None:
        _logger = Logger(environment.LOG_FILENAME, environment.ERROR_FILENAME)
    return _logger

class Logger:

    def log_info(self, message):
        if self._log_file_name is None:
            self.print_info(message)
        else:
            with open(self._log_file_name, "a") as f:
                f.write(self._info_format(message))
                f.write("\n")
        
    def log_error(self, message, err):
        if self._error_file_name is None:
            self.print_error(message, err)
        else:
            with open(self._error_file_name, "a") as f:
                f.write(self._error_format(message, err, to_file=True))
                f.write("\n")
            
    def print_info(self, message):
        print(self._info_format(message))
        
    def print_error(self, message, err):
        print(self._error_format(message, err))
        
    def _info_format(self, message):
        return f"[INFO] {message}"
        
    def _error_format(self, message, err, to_file=False):
        if not to_file:
            return f"\033[91m[ERROR] {message}: {type(err).__name__}: {err}\033[0m"
        return f"[ERROR] {message}: {type(err).__name__}: {err}"
        
    def __init__(self, log_filename, error_filename):
        self._log_file_name = log_filename
        self._error_file_name = error_filename