from colorama import Fore, Style, init

init(autoreset=True)

class RoSolveException(Exception):
    """Base exception for RoSolve API errors"""
    def __str__(self):
        return f"{Fore.RED}{super().__str__()}{Style.RESET_ALL}"

class InvalidKey(RoSolveException):
    """Raised when the API key is invalid"""
    def __str__(self):
        return f"{Fore.YELLOW}Invalid API Key: {super().__str__()}{Style.RESET_ALL}"

class TaskError(RoSolveException):
    """Raised when a task fails"""
    def __str__(self):
        return f"{Fore.RED}Task Error: {super().__str__()}{Style.RESET_ALL}"

class ProxyError(RoSolveException):
    """Raised when there's an issue with the proxy"""
    def __str__(self):
        return f"{Fore.YELLOW}Proxy Error: {super().__str__()}{Style.RESET_ALL}" 