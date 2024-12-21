from threading import Lock


class SingletonMeta(type):
    """Thread-safe Singleton metaclass."""

    _instance = None
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs) -> type:  # noqa: ANN002, ANN003
        """Create a new instance of the class if it doesn't exist."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__call__(*args, **kwargs)

            return cls._instance

        return cls._instance
