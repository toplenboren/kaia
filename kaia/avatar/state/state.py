from typing import *
from copy import deepcopy
from .memory_item import MemoryItem
from yo_fluq import Queryable
from kaia.dub import IntentsPack, Template
from kaia.dub.rhasspy_utils import RhasspyHandler

class State:
    def __init__(self, initial_state: dict[str, str]):
        self._session_id: str = ''
        self._state = deepcopy(initial_state)
        self._memory: list[MemoryItem] = []
        self._intents_pack: tuple[IntentsPack,...] = ()
        self._replies: tuple[Template,...] = ()
        self._rhasspy_handlers: Dict[str, RhasspyHandler] = {}

    def initialize_intents_and_replies(self, intents_packs: tuple[IntentsPack,...], replies: tuple[Template,...]):
        self._intents_packs = intents_packs
        self._replies = replies
        self._rhasspy_handlers = {pack.name: RhasspyHandler(pack.templates) for pack in self._intents_packs}

    @property
    def intents_packs(self):
        return self._intents_packs

    @property
    def replies(self):
        return self._replies

    @property
    def rhasspy_handlers(self):
        return self._rhasspy_handlers


    @property
    def session_id(self):
        return self._session_id

    def apply_change(self, change: dict[str, str]):
        for key, value in change.items():
            self._state[key] = value

    def get_state(self) -> dict[str, str]:
        return deepcopy(self._state)

    def add_memory(self, item: MemoryItem):
        self._memory.append(item)

    def iterate_memory_reversed(self) -> Queryable[MemoryItem]:
        return Queryable(reversed(self._memory), len(self._memory))
