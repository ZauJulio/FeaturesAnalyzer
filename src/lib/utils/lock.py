from pathlib import Path
from threading import Lock
from time import sleep


class FileLock:
    """File lock for multiprocessing and multithreading safety."""

    def __init__(self, file_path: Path, check_interval: float = 0.1) -> None:
        """
        Initialize the file lock.

        Args:
            file_path (Path): The path of the file to lock.
            check_interval (float): Time to wait (in seconds) between lock checks.

        """
        self.lock_file = file_path.with_suffix(".lock")
        self.thread_lock = Lock()
        self.check_interval = check_interval

    def __enter__(self) -> None:
        """Acquire the lock."""
        with self.thread_lock:
            while self.lock_file.exists():
                sleep(self.check_interval)  # Avoid busy-waiting

            self.lock_file.touch()

    def __exit__(self, *_: object) -> None:
        """Release the lock."""
        with self.thread_lock:
            if self.lock_file.exists():
                try:
                    self.lock_file.unlink()
                except FileNotFoundError:
                    logger.error(f"Lock file {self.lock_file} was not found.")


# Example usage:
if __name__ == "__main__":
    import threading
    from pathlib import Path

    from logger import logger

    def write_to_file(file_path: Path) -> None:
        """Write to a file using a file lock."""
        with FileLock(file_path):
            logger.info(f"Thread {threading.current_thread().name} acquired the lock.")

            with Path.open(file_path, "a", encoding="utf-8") as f:
                f.write(f"Thread {threading.current_thread().name} was here.\n")

            logger.info(f"Thread {threading.current_thread().name} released the lock.")

    file_path = Path("example_file.txt")
    threads = [
        threading.Thread(target=write_to_file, args=(file_path,)) for _ in range(5)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    logger.info("All threads have finished.")
