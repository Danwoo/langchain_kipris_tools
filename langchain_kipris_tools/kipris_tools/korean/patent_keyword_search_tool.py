from langchain_kipris_tools.kipris_api.korean import PatentFreeSearchAPI
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import typing as t
import pandas as pd


class PatentKeywordSearchArgs(BaseModel):
    word: str = Field(
        "",
        description="Technical keyword, searches Korean patent database by technology terms, use specific Korean technical keyword",
    )
    patent: bool = Field(
        True,
        description="Patent inclusion, includes patent documents in search results, set to True for patents or False to exclude",
    )
    utility: bool = Field(
        True,
        description="Utility model inclusion, includes utility model documents in search results, set to True for utility models or False to exclude",
    )
    lastvalue: str = Field(
        "",
        description="Patent status, filters patents by registration status, use status codes: empty = all patents (전체), 'A' = published (공개), 'C' = withdrawn (취하), 'F' = expired (소멸), 'G' = abandoned (포기), 'I' = invalid (무효), 'J' = rejected (거절), 'R' = registered (등록)",
    )
    docs_start: int = Field(
        1,
        description="Start index, sets starting position for result pagination, use integer starting from 0",
    )
    docs_count: int = Field(
        10,
        description="Result limit, controls number of patents returned per search, use integer between 1-100",
    )
    desc_sort: bool = Field(
        True,
        description="Sort order, controls ascending or descending order, set to True for descending (newest first) or False for ascending",
    )
    sort_spec: str = Field(
        "AD",
        description="Sort criteria, determines result ordering by date type, use date codes: empty = default relevance sorting (기본정렬), 'AD' = application date (출원일자), 'GD' = registration date (등록일자), 'PD' = publication date (공고일자), 'OPD' = open date (공개일자)",
    )

    class Config:
        safe_retry_params = {
            "critical": ["word"],
            "optional": ["docs_count", "sort_spec"],
            "safe_defaults": {
                "docs_count": [5],
                "sort_spec": "AD",
            },
        }


class PatentKeywordSearchTool(BaseTool):
    name: str = "korean_patent_info_search"
    description: str = (
        "Search Korean patent database by technical keywords for patent information analysis. Use for patent landscape research, prior art analysis, and monitoring patent trends, including those of competitors, in Korean patents"
    )
    api: PatentFreeSearchAPI = PatentFreeSearchAPI()
    args_schema: t.Type[BaseModel] = PatentKeywordSearchArgs
    return_direct: bool = False

    def _run(
        self,
        word: str,
        patent: bool = True,
        utility: bool = True,
        lastvalue: str = "",
        docs_start: int = 0,
        docs_count: int = 10,
        desc_sort: bool = True,
        sort_spec: str = "AD",
    ) -> pd.DataFrame:
        result = self.api.search(
            word,
            patent=patent,
            utility=utility,
            lastvalue=lastvalue,
            docs_start=docs_start,
            docs_count=docs_count,
            sort_spec=sort_spec,
            desc_sort=desc_sort,
        )
        return result
