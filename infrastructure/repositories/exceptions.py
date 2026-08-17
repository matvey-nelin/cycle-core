class RepositoryError(Exception):
    """Base class for repository layer exceptions"""

    error_code = "INTERNAL_REPOSITORY_ERROR"
    status_code = 500

    def __init__(self, message: str = "Internal repository error") -> None:
        self.message = message
        super().__init__(message)


class IncorrectWorkoutIdError(RepositoryError):
    """Raised when repository layer cannot found the workout by id"""

    error_code = "INCORRECT_WORKOUT_ID"
    status_code = 404

    def __init__(self, message: str = "Incorrect workout id") -> None:
        self.message = message
        super().__init__(message)


class IncorrectWorkoutSetIdError(RepositoryError):
    """Raised when repository layer cannot found the workout set by id"""

    error_code = "INCORRECT_WORKOUT_SET_ID"
    status_code = 404

    def __init__(self, message: str = "Incorrect workout set id") -> None:
        self.message = message
        super().__init__(message)


class IncorrectAgonistIdError(RepositoryError):
    """Raised when repository layer cannot found the agonist by id"""

    error_code = "INCORRECT_AGONIST_ID"
    status_code = 404

    def __init__(self, message: str = "Incorrect agonist id") -> None:
        self.message = message
        super().__init__(message)


class IncorrectExerciseIdError(RepositoryError):
    """Raised when repository layer cannot found the exercise by id"""

    error_code = "INCORRECT_EXERCISE_ID"
    status_code = 404

    def __init__(self, message: str = "Incorrect exercise id") -> None:
        self.message = message
        super().__init__(message)
