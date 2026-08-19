class DomainError(Exception):
    """Base class for domain layer exceptions"""

    error_code = "DOMAIN_ERROR"
    status_code = 422

    def __init__(self, message: str = "Internal service error") -> None:
        self.message = message
        super().__init__(message)


class DataIntegrityError(DomainError):
    """Raised when raising IntegrityError in database"""

    error_code = "DATA_INTEGRITY_ERROR"
    status_code = 409

    def __init__(self, message: str = "Data integrity error") -> None:
        self.message = message
        super().__init__(message)


class IncorrectWorkoutTimesError(DomainError):
    """Raised when start time of workout exceeds end time of workout"""

    error_code = "WORKOUT_INVALID_TIMESTAMPS"
    status_code = 422

    def __init__(self, message: str = "Workout invalid timestamps") -> None:
        self.message = message
        super().__init__(message)


class IncorrectWorkoutSetIdError(DomainError):
    """Raised when passed non-existent id of WorkoutSet"""

    error_code = "WORKOUTSET_INVALID_ID"
    status_code = 404

    def __init__(self, message: str = "WorkoutSet invalid id") -> None:
        self.message = message
        super().__init__(message)


class IncorrectOrderValueError(DomainError):
    """Raised when passed incorrect order value in constructor of WorkoutSet"""

    error_code = "INCORRECT_ORDER_VALUE"
    status_code = 422

    def __init__(self, message: str = "Incorrect order value") -> None:
        self.message = message
        super().__init__(message)


class IncorrectRepsValueError(DomainError):
    """Raised when passed incorrect reps value in constructor of WorkoutSet"""

    error_code = "INCORRECT_REPS_VALUE"
    status_code = 422

    def __init__(self, message: str = "Incorrect reps value") -> None:
        self.message = message
        super().__init__(message)


class IncorrectWeightValueError(DomainError):
    """Raised when passed incorrect weight value in constructor of WorkoutSet"""

    error_code = "INCORRECT_WEIGHT_VALUE"
    status_code = 422

    def __init__(self, message: str = "Incorrect weight value") -> None:
        self.message = message
        super().__init__(message)


class IncorrectAgonistNameError(DomainError):
    """Raised when passed incorrect name in constructor of Agonist"""

    error_code = "INCORRECT_AGONIST_NAME"
    status_code = 422

    def __init__(self, message: str = "Incorrect agonist name") -> None:
        self.message = message
        super().__init__(message)


class IncorrectExerciseNameError(DomainError):
    """Raised when passed incorrect name in constructor of Exercise"""

    error_code = "INCORRECT_EXERCISE_NAME"
    status_code = 422

    def __init__(self, message: str = "Incorrect exercise name") -> None:
        self.message = message
        super().__init__(message)


class DuplicateAgonistIdError(DomainError):
    """Raised when adds already existing 'agonist_id' in exercise"""

    error_code = "DUPLICATE_AGONIST_ID"
    status_code = 409

    def __init__(self, message: str = "Duplicate 'agonist_id'") -> None:
        self.message = message
        super().__init__(message)


class NonExistentAgonistIdError(DomainError):
    """Raised when removes non-existent 'agonist_id' of exercise"""

    error_code = "NON_EXISTENT_AGONIST_ID"
    status_code = 404

    def __init__(self, message: str = "Non-existent 'agonist_id'") -> None:
        self.message = message
        super().__init__(message)
