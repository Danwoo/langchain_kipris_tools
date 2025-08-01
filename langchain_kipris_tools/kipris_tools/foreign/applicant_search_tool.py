from langchain_kipris_tools.kipris_api.foreign import ForeignPatentApplicantSearchAPI
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import typing as t
import pandas as pd
from langchain_kipris_tools.kipris_api.foreign.code import count_dict, sort_field_dict
from logging import getLogger

logger = getLogger(__name__)


class ForeignPatentApplicantSearchArgs(BaseModel):
    applicant: str = Field(
        "",
        description="Company name, searches international patents by applicant organization, use English company names or original language company names (e.g., 'Samsung Electronics', 'Toyota Motor', 'Microsoft Corporation')",
    )
    current_page: int = Field(
        1,
        description="Page number, sets current page for pagination, use integer starting from 1",
    )
    sort_field: str = Field(
        "AD",
        description="Sort criteria, determines result ordering by date type, use date codes: 'AD' = application date (출원일자), 'GD' = registration date (등록일자), 'PD' = publication date (공고일자), 'OPD' = open date (공개일자)",
    )
    sort_state: bool = Field(
        True,
        description="Sort order, controls ascending or descending order, set to True for descending (newest first) or False for ascending",
    )
    collection_values: str = Field(
        "US",
        description="Country database, specifies target patent database by country, select exactly **one** of the following country codes: 'US' = United States, 'EP' = Europe, 'WO' = PCT, 'JP' = Japan, 'PJ' = Japan English Abstract, 'CP' = China, 'CN' = China English Abstract, 'TW' = Taiwan English Abstract, 'RU' = Russia, 'CO' = Colombia, 'SE' = Sweden, 'ES' = Spain, 'IL' = Israel",
    )

    class Config:
        safe_retry_params = {
            "critical": ["applicant"],
            "optional": ["sort_field", "collection_values"],
            "safe_defaults": {
                "sort_field": "AD",
                "collection_values": "US",
                "sort_state": True,
            },
        }


class ForeignPatentApplicantSearchTool(BaseTool):
    name: str = "international_patent_company_search"
    description: str = (
        "Search international patents by company or organization name. Use for analyzing global patent portfolios of specific companies across multiple countries."
    )
    api: ForeignPatentApplicantSearchAPI = ForeignPatentApplicantSearchAPI()
    args_schema: t.Type[BaseModel] = ForeignPatentApplicantSearchArgs
    return_direct: bool = False

    def _run(
        self,
        applicant: str,
        current_page: int = 1,
        sort_field: str = "AD",
        sort_state: bool = True,
        collection_values: str = "US",
        **kwargs,
    ) -> pd.DataFrame:
        if not applicant:
            raise ValueError("international_open_number is required")
        if collection_values not in count_dict:
            raise ValueError(f"collection_values must be in {count_dict.keys()}")
        if sort_field not in sort_field_dict:
            raise ValueError(f"sort_field must be in {sort_field_dict.keys()}")
        # logger.info(f"applicant: {applicant}")

        result = self.api.search(
            applicant=applicant,
            current_page=current_page,
            sort_field=sort_field,
            sort_state=sort_state,
            collection_values=collection_values,
            **kwargs,
        )
        return result
