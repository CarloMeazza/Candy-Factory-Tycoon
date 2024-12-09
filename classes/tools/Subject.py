from typing import List, Callable, Dict, Any, Tuple

# Alias di tipo per semplificare le annotazioni
Observer = Callable[..., None]
ObserversList = List[Tuple[int, Observer]]


class Subject:
    """
    Singleton class implementing the Observer pattern.
    Allows multiple observers to be registered and notified when events occur.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_observers"):
            self._observers: Dict[str, ObserversList] = {}

    def attach(self, event_type: str, observer: Observer, priority: int = 0) -> None:
        """
        Registers an observer for a specific event type, with optional priority.

        Args:
            event_type (str): The type of event the observer is interested in.
            observer (Observer): The observer function to be notified when the event occurs.
            priority (int, optional): The priority of the observer. Higher values indicate
                                      higher priority. Defaults to 0.
        """
        self._observers.setdefault(event_type, []).append((priority, observer))
        self._observers[event_type].sort(key=lambda x: -x[0])

    def detach(self, event_type: str, observer: Observer) -> None:
        """
        Removes an observer for a specific event type.

        Args:
            event_type (str): The type of event the observer is interested in.
            observer (Observer): The observer function to be removed.
        """
        if event_type in self._observers:
            self._observers[event_type] = [
                o for o in self._observers[event_type] if o[1] != observer
            ]

    def notify(self, event_type: str, *args: Any, **kwargs: Any) -> None:
        """
        Notifies all observers registered for the given event type.

        Args:
            event_type (str): The type of event to notify observers about.
            *args (Any): Additional positional arguments to be passed to the observers.
            **kwargs (Any): Additional keyword arguments to be passed to the observers.
        """
        for _, observer in self._observers.get(event_type, []):
            observer(*args, **kwargs)
