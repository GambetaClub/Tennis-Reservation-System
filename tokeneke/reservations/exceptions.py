class ActivityCreationError(Exception):
    """Custom exception for errors during activity creation."""

    def __init__(self, message):
        super().__init__(message)


class ActivityUpdateError(Exception):
    """Custom exception for errors during activity update."""

    def __init__(self, message):
        super().__init__(message)


class DateCreationError(Exception):
    """Custom exception for errors during date creation."""

    def __init__(self, message):
        super().__init__(message)


class DateUpdateError(Exception):
    """Custom exception for errors during date update."""

    def __init__(self, message):
        super().__init__(message)
