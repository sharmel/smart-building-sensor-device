class SensorError(Exception):
    """Base application exception."""


class OutOfOrderReadingError(SensorError):
    """Reading timestamp is not newer than the latest stored reading."""


class SensorError(Exception):
    """Base application exception."""


class OutOfOrderReadingError(SensorError):
    """Reading is older than the stored reading."""


class DuplicateReadingError(SensorError):
    """Reading timestamp already exists."""


class SensorNotFoundError(SensorError):
    """Sensor does not exist."""


class InvalidSensorValueError(SensorError):
    """Sensor value violates business rules."""
