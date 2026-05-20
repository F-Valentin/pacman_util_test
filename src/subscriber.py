from typing import Protocol


class IPacgumSubscriber(Protocol):
    def on_pacgum_eaten(self) -> None: ...

    def on_super_pacgum_eaten(self) -> None: ...


class IPlayerDeathSubscriber(Protocol):
    def on_player_death(self) -> None: ...


class IPlayerSubscriber(Protocol):
    ...


class ILevelManagerSubscriber(Protocol):
    def on_all_levels_completed(self) -> None: ...


class IGhostSubscriber(Protocol):
    def on_ghost_death(self) -> None: ...
