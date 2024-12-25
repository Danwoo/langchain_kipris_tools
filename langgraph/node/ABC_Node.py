from abc import * 
from typing import TypedDict, List, Any
from langgraph.graph import StateGraph, START, END
from logging import getLogger

logger = getLogger(__name__)

class NodeTemplate(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def _pre_execute(self, state:Any, **kwargs):
        pass 

    @abstractmethod
    def _post_execute(self, state:Any, **kwargs):
        pass 
        
    def __call__(self, state:Any, **kwargs)->Any:   
        logger.info(f"Node {self.__class__.__name__} is called")        
        self._pre_execute(state, **kwargs)
        self.result = self.execute(state, **kwargs)
        self._post_execute(state, **kwargs)
        return self.result
        
    @abstractmethod
    def execute(self, state:Any, **kwargs)->Any:
        pass 
    