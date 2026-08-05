class DomainError(Exception):
    """Base class for domain layer exceptions"""

    error_code = "INTERNAL_SERVER_ERROR"
    status_code = 500

    def __init__(self, message: str = "Internal service error") -> None:
        self.message = message
        super().__init__(message)


class IncorrectWorkoutTimesError(DomainError):
    """Raised when start time of workout exceeds end time of workout"""

    error_code = "WORKOUT_INVALID_TIMESTAMPS"
    status_code = 400

    def __init__(self, message: str = "Workout invalid timestamps") -> None:
        self.message = message
        super().__init__(message)
