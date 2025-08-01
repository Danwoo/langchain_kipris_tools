from langchain_kipris_tools.kipris_api.korean import PatentDetailSearchAPI
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import typing as t
import pandas as pd


class PatentDetailSearchArgs(BaseModel):
    application_number: str = Field(
        "",
        description="Application number, retrieves detailed patent information by exact application number, use Korean patent application number format (10-13 digits, e.g., '1020210012345')",
    )

    class Config:
        safe_retry_params = {
            "critical": ["application_number"],
            "optional": [],
            "safe_defaults": {},
        }


class PatentDetailSearchTool(BaseTool):
    name: str = "korean_patent_detail_lookup"
    description: str = (
        "Get comprehensive patent details by providing an exact application number. Use this tool for full patent specification, claims, and technical documentation analysis."
    )
    api: PatentDetailSearchAPI = PatentDetailSearchAPI()
    args_schema: t.Type[BaseModel] = PatentDetailSearchArgs
    return_direct: bool = False

    def _run(self, application_number: str) -> pd.DataFrame:
        if not application_number:
            raise ValueError("you must provide application_number")

        result = self.api.search(application_number=application_number)
        return result
