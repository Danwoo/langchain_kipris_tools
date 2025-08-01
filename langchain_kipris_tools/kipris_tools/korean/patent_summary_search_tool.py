from langchain_kipris_tools.kipris_api.korean import PatentSummarySearchAPI
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import typing as t
import pandas as pd


class PatentSummarySearchArgs(BaseModel):
    application_number: str = Field(
        "",
        description="Application number, retrieves patent summary by exact application number, use Korean patent application number format (10-13 digits, e.g., '1020210012345')",
    )

    class Config:
        safe_retry_params = {
            "critical": ["application_number"],
            "optional": [],
            "safe_defaults": {},
        }


class PatentSummarySearchTool(BaseTool):
    name: str = "korean_patent_summary_lookup"
    description: str = (
        "Get patent summary information by providing an exact application number. Use this tool for a quick patent overview and abstract details."
    )
    api: PatentSummarySearchAPI = PatentSummarySearchAPI()
    args_schema: t.Type[BaseModel] = PatentSummarySearchArgs
    return_direct: bool = False

    def _run(self, application_number: str) -> pd.DataFrame:
        if not application_number:
            raise ValueError("you must provide application_number")

        result = self.api.search(application_number=application_number)
        return result
