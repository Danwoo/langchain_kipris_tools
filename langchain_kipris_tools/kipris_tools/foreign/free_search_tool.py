from langchain_kipris_tools.kipris_api.foreign import ForeignPatentFreeSearchAPI
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import typing as t
import pandas as pd
from langchain_kipris_tools.kipris_api.foreign.code import count_dict, sort_field_dict


class ForeignPatentFreeSearchArgs(BaseModel):
    free: str = Field(
        "",
        description="English keywords, searches international patent databases using English technical terms, must use English only (e.g., 'biomass polymerization', 'eco-friendly fiber', 'semiconductor device')",
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
            "critical": ["free"],  # 검색어는 반드시 필요
            "optional": [
                "sort_field",
                "collection_values",
            ],  # 정렬과 국가는 중요하지만 선택사항
            "safe_defaults": {
                "sort_field": "AD",  # 최신 출원일 정렬로 고정
                "sort_state": True,  # 내림차순 정렬 (최신순)
                "collection_values": "US",  # 미국 특허로 고정 (가장 많은 데이터)
            },
        }


class ForeignPatentFreeSearchTool(BaseTool):
    name: str = "international_patent_info_search"
    description: str = (
        "Search international patent databases using English keywords. Select one of the listed two-letter country/regional codes to search."
    )
    api: ForeignPatentFreeSearchAPI = ForeignPatentFreeSearchAPI()
    args_schema: t.Type[BaseModel] = ForeignPatentFreeSearchArgs
    return_direct: bool = False

    def _run(
        self,
        free: str,
        current_page: int = 1,
        sort_field: str = "AD",
        sort_state: bool = True,
        collection_values: str = "US",
        **kwargs,
    ) -> pd.DataFrame:
        if not free:
            raise ValueError("free is required")
        if collection_values not in count_dict:
            raise ValueError(f"collection_values must be in {count_dict.keys()}")
        if sort_field not in sort_field_dict:
            raise ValueError(f"sort_field must be in {sort_field_dict.keys()}")
        result = self.api.search(
            free=free,
            current_page=current_page,
            sort_field=sort_field,
            sort_state=sort_state,
            collection_values=collection_values,
            **kwargs,
        )
        return result
