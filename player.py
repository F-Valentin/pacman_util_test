from subsriber import IPlayerSubscriber

class Player:
    def __init__(self) -> None:
        self._subscribers: list[IPlayerSubscriber] = []

    @property
    def subscribers(self) -> list[IPlayerSubscriber]:
        return self._subscribers

    def add_subscriber(self, subscriber: IPlayerSubscriber) -> None:
        self._subscribers.append(subscriber) 

    def remove_subscriber(self, subscriber: IPlayerSubscriber) -> None:
        self._subscribers.remove(subscriber) 
    
    def die(self) -> None:
        for subscriber in self._subscribers:
            subscriber.on_player_death()
    
    def eat_pacgum(self) -> None:
        for subscriber in self._subscribers:
            subscriber.on_player_ate_super_pacgum()
    
    def level_completed(self) -> None:
        for subscriber in self._subscribers:
            subscriber.on_player_completed_level()


player = Player()

player.die()
player.level_completed()