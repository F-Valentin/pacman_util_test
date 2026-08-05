import os

import hjson


class GameConfig:
    """Load and validate runtime settings from the configuration file."""

    def __init__(self, file_path: str):
        self.file_path = file_path

        self.custom = False
        self.lives = 3
        self.level_max_time = 90

        self.points_per_pacgum = 5
        self.points_per_super_pacgum = 100
        self.points_per_ghost = 200

        self.screen_width = 900
        self.screen_height = 900
        self.tile_size: int = 60

        self.raw_data: dict[str, int | bool] = {}

        self._load_config()

    @staticmethod
    def _parse_bool(value: object, key: str) -> bool:
        """Validate and return a boolean configuration value."""
        if not isinstance(value, bool):
            raise TypeError(
                f"'{key}' must be a boolean (true/false), "
                f"got {type(value).__name__!r} instead.")

        return value

    @staticmethod
    def _parse_int(value: object, key: str) -> int:
        """Validate and return an integer configuration value."""
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(
                f"'{key}' must be an integer, "
                f"got {type(value).__name__!r} instead.")
        return value

    def _load_config(self) -> None:
        """Read the JSON file and apply any custom gameplay values."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(
                f"Configuration file '{self.file_path}' not found.")

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.raw_data = hjson.load(f)
        except hjson.HjsonDecodeError as e:
            raise ValueError("The file provided is not a valid JSON.") from e
        except PermissionError as e:
            raise PermissionError(
                "Permission denied when accessing the config file.") from e

        self.custom = self._parse_bool(
            self.raw_data.get("custom", False), "custom")
        if self.custom:
            self.lives = self._parse_int(
                self.raw_data.get("lives", 3), "lives")
            self.level_max_time = self._parse_int(
                self.raw_data.get("level_max_time", 90), "level_max_time")
