import os

import hjson


class GameConfig:
    """Load and validate runtime settings from the configuration file."""

    MIN_LIVES = 1
    MAX_LIVES = 10
    MIN_LEVEL_MAX_TIME = 1
    MAX_LEVEL_MAX_TIME = 1000

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

    @staticmethod
    def _parse_bounded_int(value: object, key: str, default: int,
                           minimum: int = 1,
                           maximum: int | None = None) -> int:
        """
            Validate an integer configuration value that must fall
            within [minimum, maximum]. ``maximum=None`` means no
            upper bound.

            Reuses ``_parse_int`` for the type check, then falls back
            to ``default`` if the value is out of range (e.g. zero or
            negative lives/time, or a value above the allowed cap).
        """
        parsed = GameConfig._parse_int(value, key, default)

        if parsed < minimum or (maximum is not None and parsed > maximum):
            bound = (
                f">= {minimum}" if maximum is None
                else f"between {minimum} and {maximum}"
            )
            print(
                f"[Config Warning] '{key}' must be an integer {bound}, "
                f"got {parsed}. Using default: {default}."
            )
            return default

        return parsed

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
            self.lives = self._parse_bounded_int(
                self.raw_data.get("lives", self.lives),
                "lives", default=self.lives,
                minimum=self.MIN_LIVES, maximum=self.MAX_LIVES)
            self.level_max_time = self._parse_bounded_int(
                self.raw_data.get("level_max_time", self.level_max_time),
                "level_max_time", default=self.level_max_time,
                minimum=self.MIN_LEVEL_MAX_TIME,
                maximum=self.MAX_LEVEL_MAX_TIME)
            # 0 is a valid, meaningful seed (it means "random maze" -
            # see MazeGenerator.generate), so only negative values are
            # rejected here; there's no natural upper bound to cap.
            self.seed = self._parse_bounded_int(
                self.raw_data.get("seed", self.seed),
                "seed", default=self.seed, minimum=0)
