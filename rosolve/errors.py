class RoSolveException(Exception):
    """Base exception for RoSolve API errors"""
    pass

class InvalidKey(RoSolveException):
    """Raised when the API key is invalid"""
    pass

class TaskError(RoSolveException):
    """Raised when a task fails"""
    pass 