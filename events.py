from collections import defaultdict
import asyncio

class EventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)
        
    def subscribe(self, event_type, handler):
        self.subscribers[event_type].append(handler)
        
    def dispatch(self, event_type, *args, **kwargs):
        for handler in self.subscribers[event_type]:
            if asyncio.iscoroutinefunction(handler):
                asyncio.create_task(handler(*args))  # run async handlers
            else:
                handler(*args)  # run normal functions

bus = EventBus()