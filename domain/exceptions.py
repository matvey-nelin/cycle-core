class DomainError(Exception):
    """Base class for domain layer exceptions"""

    error_code = "INTERNAL_SERVER_ERROR"
    status_code = 500

    def __init__(self, message: str = "Internal service error") -> None:
        self.message = message
        super().__init__(message)


class DataIntegrityError(DomainError):
    """Raised when passed non-existent id of WorkoutSet"""

    error_code = "DATA_INTEGRITY_ERROR"
    status_code = 400

    def __init__(self, message: str = "Data integrity error") -> None:
        self.message = message
        super().__init__(message)


class IncorrectWorkoutTimesError(DomainError):
    """Raised when start time of workout exceeds end time of workout"""

    error_code = "WORKOUT_INVALID_TIMESTAMPS"
    status_code = 400

    def __init__(self, message: str = "Workout invalid timestamps") -> None:
        self.message = message
        super().__init__(message)


class IncorrectWorkoutSetIdError(DomainError):
    """Raised when passed non-existent id of WorkoutSet"""

    error_code = "WORKOUTSET_INVALID_ID"
    status_code = 400

    def __init__(self, message: str = "WorkoutSet invalid id") -> None:
        self.message = message
        super().__init__(message)


class DuplicateAgonistIdError(DomainError):
    """Raised when adds already existing 'agonist_id' in exercise"""

    error_code = "DUPLICATE_AGONIST_ID"
    status_code = 400

    def __init__(self, message: str = "Duplicate 'agonist_id'") -> None:
        self.message = message
        super().__init__(message)


class NonExistentAgonistIdError(DomainError):
    """Raised when removes non-existent 'agonist_id' of exercise"""

    error_code = "NON_EXISTENT_AGONIST_ID"
    status_code = 400

    def __init__(self, message: str = "Non-existent 'agonist_id'") -> None:
        self.message = message
        super().__init__(message)
