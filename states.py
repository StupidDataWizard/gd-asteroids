from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self):
        self.new_state = None

    def update(self, _):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

    def process_event(self, event):
        pass

    def next_state(self):
        if self.new_state is None:
            return None
        else:
            state = self.new_state
            self.new_state = None
            return state


class EmptyState(State):
    def draw(self, surface):
        pass
