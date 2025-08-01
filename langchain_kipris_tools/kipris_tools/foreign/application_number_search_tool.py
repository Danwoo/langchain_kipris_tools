from langchain_kipris_tools.kipris_api.foreign import (
    ForeignPatentApplicationNumberSearchAPI,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import typing as t
import pandas as pd
from langchain_kipris_tools.kipris_api.foreign.code import count_dict, sort_field_dict


class ForeignPatentApplicationNumberSearchArgs(BaseModel):
    application_number: str = Field(
        "",
        description="Application number, looks up specific international patent by exact application number, use country-specific patent application number format (e.g., US: '16/123456', EP: 'EP19123456')",
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
            "critical": ["application_number"],
            "optional": ["sort_field", "collection_values"],
            "safe_defaults": {
                "sort_field": "AD",
                "collection_values": "US",
                "sort_state": True,
            },
        }


class ForeignPatentApplicationNumberSearchTool(BaseTool):
    name: str = "international_patent_number_lookup"
    description: str = (
        "Look up specific international patent by application number. Use for direct patent information retrieval from US, EP, JP, CN and other patent offices."
    )
    api: ForeignPatentApplicationNumberSearchAPI = (
        ForeignPatentApplicationNumberSearchAPI()
    )
    args_schema: t.Type[BaseModel] = ForeignPatentApplicationNumberSearchArgs
    return_direct: bool = False

    def _run(
        self,
        application_number: str,
        current_page: int = 1,
        sort_field: str = "AD",
        sort_state: bool = True,
        collection_values: str = "US",
        **kwargs,
    ) -> pd.DataFrame:
        if not application_number:
            raise ValueError("application_number is required")
        if collection_values not in count_dict:
            raise ValueError(f"collection_values must be in {count_dict.keys()}")
        if sort_field not in sort_field_dict:
            raise ValueError(f"sort_field must be in {sort_field_dict.keys()}")
        result = self.api.search(
            application_number=application_number,
            current_page=current_page,
            sort_field=sort_field,
            sort_state=sort_state,
            collection_values=collection_values,
            **kwargs,
        )
        return result
