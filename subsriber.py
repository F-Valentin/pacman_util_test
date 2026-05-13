from abc import ABC, abstractmethod

class ISubcriber(ABC):
    @abstractmethod
    def add_subscriber(self):
        pass

    @abstractmethod
    def remove_subscriber(self):
        pass

class IPlayerSubscriber(ISubcriber):
    def add_subscriber(self):
        pass
    
    def remove_subscriber(self):
        pass

    @abstractmethod
    def on_player_death(self):
        pass

    @abstractmethod
    def on_player_ate_super_pacgum(self):
        pass

    @abstractmethod
    def on_player_complete_level(self):
        pass


class IGhostSubscriber(ISubcriber):
    def add_subscriber(self):
        pass
    
    def remove_subscriber(self):
        pass

    @abstractmethod
    def on_ghost_dead(self):
        pass