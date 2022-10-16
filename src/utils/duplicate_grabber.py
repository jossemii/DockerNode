from time import time
from typing import Any, Dict, Generator, List, Tuple
from uuid import uuid4
from threading import Event, Lock

from src.utils.singleton import Singleton
from src.utils import logger as l

from protos import celaut_pb2 as celaut

class Session:
    
    def __init__(self) -> None:
        self.event: Event = Event()
        self.value: List = []
        self.end_time = None

    def wait(self):
        self.event.wait()

    def set(self):
        self.event.set()
        self.end_time = time()

class DuplicateGrabber(metaclass=Singleton):

    def __init__(self):
        self.hashes: Dict[str, str] = {}
        self.sessions: Dict[str: Session ] = {}
        self.lock = Lock()

    def manager(self, completion_time: float = 1):
        for session in self.sessions.keys():
            end_time: float = self.sessions[session].end_time
            if end_time and \
                time() - end_time > completion_time:
                del self.sessions[session]

    def next(self,
        hashes: List[celaut.Any.Metadata.HashTag.Hash],
        generator: Generator
    ) -> Tuple[Any, bool]:

        # hash.type.decode('utf-8')+':'+hash.value.decode('utf-8')  
        #  UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte
        hashes: List[str] = [str(hash_element) for hash_element in hashes]
        wait: bool = False

        with self.lock:
            for hash_element in hashes:
                if hash_element in self.hashes.keys():
                    session = self.hashes[hash_element]
                    wait = True
                    break
            
            if not wait:
                session = uuid4().hex
                for hash_element in hashes:
                    self.hashes[hash_element] = session
                self.sessions[session] = Session()

        if wait:
            if self.sessions[session].end_time:
                return self.sessions[session].value, False
            l.LOGGER('It is already downloading. waiting for it to end. '+session)
            self.sessions[session].wait()
            return self.sessions[session].value, False

        else:
            l.LOGGER('Start download '+session)
            self.sessions[session].value = next(generator)
            self.sessions[session].set()
            return self.sessions[session].value, True
