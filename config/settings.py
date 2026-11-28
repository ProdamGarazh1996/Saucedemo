import os
from dataclasses import dataclass


def _env_window_size() -> tuple[int, int]:
    width, height = os.getenv("WINDOW_SIZE", "1920,1080").split(",")
    return int(width), int(height)


@dataclass(frozen=True)
class Settings:
    base_url: str
    timeout: int
    window_size: tuple[int, int]
    password: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            base_url=os.getenv("BASE_URL",
                               "https://www.saucedemo.com").rstrip("/"),
            timeout=int(os.getenv("TIMEOUT", "10")),
            window_size=_env_window_size(),
            password=os.getenv("SAUCE_PASSWORD", "secret_sauce"),
        )


settings = Settings.from_env()
