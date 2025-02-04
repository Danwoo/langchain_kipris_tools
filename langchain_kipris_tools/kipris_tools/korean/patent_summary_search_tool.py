from langchain_kipris_tools.kipris_api.korean import PatentSummarySearchAPI
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import typing as t
import pandas as pd

class PatentSummarySearchArgs(BaseModel):
    application_number: str = Field("", description="Application number")    

class PatentSummarySearchTool(BaseTool):
    name:str = "korean_patent_summary_search"
    description:str = "patent summary search. you provide application number then it will return patent summary"
    api:PatentSummarySearchAPI = PatentSummarySearchAPI()
    args_schema:t.Type[BaseModel] = PatentSummarySearchArgs
    return_direct: bool = False
    
    def _run(self, application_number:str)->pd.DataFrame:
        if not application_number:
            raise ValueError("you must provide application_number")
            
        result = self.api.search(application_number=application_number)
        return result
