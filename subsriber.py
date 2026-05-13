from abc import ABC, abstractmethod

class ISubcriber(ABC):
    def __init__(self):
        self.subscribers = []

    @abstractmethod
    def add_subscriber(self):
        pass

    @abstractmethod
    def remove_subscriber(self):
        pass

class IPlayerSubscriber(ABC, ISubcriber):
    @abstractmethod
    def on_player_death(self):
        pass

    @abstractmethod
    def on_player_ate_super_pacgum(self):
        pass

    @abstractmethod
    def on_player_complete_level(self):
        pass


class IGhostSubscriber(ABC, ISubcriber):
    @abstractmethod
    def on_ghost_dead(self):
        pass