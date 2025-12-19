from abc import ABC, abstractmethod
from aiogram import Router


class BaseRoute(ABC):
    """Базовый класс для всех роутов"""
    
    def __init__(self, router: Router):
        self.router = router
        self.register_handlers()
    
    @abstractmethod
    def register_handlers(self):
        pass