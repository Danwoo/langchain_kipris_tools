from langchain_kipris_tools.kipris_api.korean import PatentDetailSearchAPI
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import typing as t
import pandas as pd


class PatentDetailSearchArgs(BaseModel):
    application_number: str = Field("", description="Application number")

    class Config:
        safe_retry_params = {
            "critical": ["application_number"],
            "optional": [],
            "safe_defaults": {},
        }


class PatentDetailSearchTool(BaseTool):
    name: str = "korean_patent_detail_search"
    description: str = (
        "patent detail search. you provide application number then it will return patent detail"
    )
    api: PatentDetailSearchAPI = PatentDetailSearchAPI()
    args_schema: t.Type[BaseModel] = PatentDetailSearchArgs
    return_direct: bool = False

    def _run(self, application_number: str) -> pd.DataFrame:
        if not application_number:
            raise ValueError("you must provide application_number")

        result = self.api.search(application_number=application_number)
        return result
