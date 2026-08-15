import os

import hjson


class GameConfig:
    """Load and validate runtime settings from the configuration file."""

    def __init__(self, file_path: str):
        self.file_path = file_path

        self.custom = False
        self.lives = 3
        self.level_max_time = 90
        self.seed = 42

        self.points_per_pacgum = 5
        self.points_per_super_pacgum = 100
        self.points_per_ghost = 200

        self.screen_width = 900
        self.screen_height = 900
        self.tile_size: int = 60

        self.raw_data: dict[str, int | bool] = {}

        self._load_config()

    @staticmethod
    def _parse_bool(value: object, key: str, default: bool) -> bool:
        """
            Validate a boolean configuration value.

            On an invalid type, log a warning and fall back
            to ``default`` instead of raising.
        """
        if not isinstance(value, bool):
            print(
                f"[Config Warning] '{key}' must be a boolean (true/false), "
                f"got {type(value).__name__!r}. Using default: {default}."
            )
            return default

        return value

    @staticmethod
    def _parse_int(value: object, key: str, default: int) -> int:
        """
            Validate an integer configuration value.

            On an invalid type, log a warning and fall back
            to ``default`` instead of raising.
        """
        if not isinstance(value, int) or isinstance(value, bool):
            print(
                f"[Config Warning] '{key}' must be an integer, "
                f"got {type(value).__name__!r}. Using default: {default}."
            )
            return default
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

        if not isinstance(self.raw_data, dict):
            print(
                "[Config Warning] Configuration root must be a JSON "
                "object. Ignoring its content and using defaults."
            )
            self.raw_data = {}

        self.custom = self._parse_bool(
            self.raw_data.get("custom", False), "custom", default=False)

        if self.custom:
            self.lives = self._parse_int(
                self.raw_data.get("lives", self.lives),
                "lives", default=self.lives)
            self.level_max_time = self._parse_int(
                self.raw_data.get("level_max_time", self.level_max_time),
                "level_max_time", default=self.level_max_time)
            self.seed = self._parse_int(
                self.raw_data.get("seed", self.seed),
                "seed", default=self.seed)
