from abc import ABC, abstractmethod


class IPlayerSubscriber(ABC):
    @abstractmethod
    def on_player_death(self):
        pass

    @abstractmethod
    def on_player_ate_super_pacgum(self):
        pass

    @abstractmethod
    def on_player_completed_level(self):
        pass


class IGhostSubscriber(ABC):
    @abstractmethod
    def on_ghost_death(self):
        pass
