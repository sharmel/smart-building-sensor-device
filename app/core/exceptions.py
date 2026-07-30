class SensorError(Exception):
    """Base application exception."""


class OutOfOrderReadingError(SensorError):
    """Reading timestamp is not newer than the latest stored reading."""
