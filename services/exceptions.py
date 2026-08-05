class ServiceError(Exception):
    """Base class for service layer exceptions"""

    error_code = "INTERNAL_SERVER_ERROR"
    status_code = 500

    def __init__(self, message: str = "Internal service error") -> None:
        self.message = message
        super().__init__(message)


class WorkoutNotFoundError(ServiceError):
    """Raised when service layer cannot found the workout by id"""

    error_code = "WORKOUT_NOT_FOUND"
    status_code = 404

    def __init__(self, message: str = "Workout not found") -> None:
        self.message = message
        super().__init__(message)
