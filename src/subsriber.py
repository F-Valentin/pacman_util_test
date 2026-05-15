from typing import Protocol


class IPacgumSubscriber(Protocol):
    def on_pacgum_eaten(self) -> None: ...

    def on_super_pacgum_eaten(self) -> None: ...

class IPlayerDeathSubscriber(Protocol):
    def on_player_death(self) -> None: ...

class IPlayerSubscriber(Protocol): 
    def kaka(self): ...


class IGhostSubscriber(Protocol):
    def on_ghost_death(self) -> None: ...
