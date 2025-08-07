from langchain_kipris_tools.kipris_api.korean import PatentSearchAPI
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import typing as t
import pandas as pd


class PatentSearchArgs(BaseModel):
    word: str = Field(
        "",
        description="General keywords, searches across all patent fields including title and abstract, use Korean technology terms for broad patent search",
    )
    invention_title: str = Field(
        "",
        description="Patent title, searches specifically in patent invention titles, use exact or partial Korean patent title",
    )
    abst_cont: str = Field(
        "",
        description="Abstract content, searches patent abstract sections, use Korean technical descriptions found in patent abstracts",
    )
    claim_scope: str = Field(
        "",
        description="Claim content, searches patent claims sections, use Korean technical terms from patent claims",
    )

    # Classification and numbers
    ipc_number: str = Field(
        "",
        description="IPC classification, searches by International Patent Classification number, use standard IPC format (e.g., 'H01L21/00')",
    )
    application_number: str = Field(
        "",
        description="Application number, looks up patent by specific application number, use exact Korean patent application number format (10-13 digits)",
    )
    open_number: str = Field(
        "",
        description="Publication number, searches by patent publication number, use exact Korean publication number format",
    )
    register_number: str = Field(
        "",
        description="Registration number, searches by patent registration number, use exact Korean registration number format",
    )
    priority_application_number: str = Field(
        "",
        description="Priority application number, searches by priority application number from first filing, use exact priority application number format",
    )
    international_application_number: str = Field(
        "",
        description="PCT application number, searches by international PCT application number, use PCT format (e.g., 'PCT/KR2023/001234')",
    )
    international_open_number: str = Field(
        "",
        description="PCT publication number, searches by international PCT publication number, use PCT publication format (e.g., 'WO2023/123456')",
    )

    # Date fields
    application_date: str = Field(
        "",
        description="Application date, searches patents filed on specific date, use YYYY-MM-DD format (e.g., '2023-01-15')",
    )
    open_date: str = Field(
        "",
        description="Publication date, searches patents published on specific date, use YYYY-MM-DD format (e.g., '2023-06-15')",
    )
    publication_date: str = Field(
        "",
        description="Gazette date, searches patents published in gazette on specific date, use YYYY-MM-DD format (e.g., '2023-08-15')",
    )
    register_date: str = Field(
        "",
        description="Registration date, searches patents registered on specific date, use YYYY-MM-DD format (e.g., '2023-12-15')",
    )
    priority_application_date: str = Field(
        "",
        description="Priority date, searches patents with priority date, use YYYY-MM-DD format (e.g., '2022-01-15')",
    )
    international_application_date: str = Field(
        "",
        description="PCT filing date, searches patents filed under PCT on specific date, use YYYY-MM-DD format (e.g., '2023-03-15')",
    )
    international_open_date: str = Field(
        "",
        description="PCT publication date, searches PCT patents published on specific date, use YYYY-MM-DD format (e.g., '2023-09-15')",
    )

    # People and organizations
    applicant: str = Field(
        "",
        description="Company name, searches patents by applicant organization, use exact Korean company names (e.g., '삼성전자주식회사', '현대자동차')",
    )
    inventor: str = Field(
        "",
        description="Inventor name, searches patents by inventor name, use Korean inventor names",
    )
    agent: str = Field(
        "",
        description="Patent agent, searches patents by patent attorney or agent name, use Korean patent agent names",
    )
    right_holder: str = Field(
        "",
        description="Patent owner, searches patents by current patent rightholder name, use exact Korean company or individual names who currently own the patents",
    )

    # Document type filters
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
        description="Patent status, filters patents by registration status, use status codes: empty = all patents (전체), 'A' = published (공개), 'C' = withdrawn (취하), 'F' = expired (소멸), 'G' = abandoned (포기), 'I' = invalid (무효), 'J' = rejected (거절), 'R' = registered (등록). Default is empty (전체) to include all statuses.",
    )

    # Pagination and sorting
    page_no: int = Field(
        1,
        description="Page number, sets current page for pagination, use integer starting from 1",
    )
    num_of_rows: int = Field(
        10,
        description="Results per page, controls number of patents returned per page, use integer between 1-100",
    )
    desc_sort: bool = Field(
        True,
        description="Sort order, controls ascending or descending order, set to True for descending (newest first) or False for ascending",
    )
    sort_spec: str = Field(
        "",
        description="Sort criteria, determines result ordering by date type, use date codes: ** IMPORTANT: Default to empty string ('') when user doesn't specify sorting ** '' = default sorting (기본정렬), 'AD' = application date (출원일자), 'GD' = registration date (등록일자), 'PD' = publication date (공고일자), 'OPD' = open date (공개일자). ** Use empty string ('') unless explicitly requested otherwise **",
    )

    class Config:
        safe_retry_params = {
            "critical": ["word", "applicant", "invention_title"],
            "optional": ["num_of_rows", "sort_spec", "abst_cont"],
            "safe_defaults": {
                "num_of_rows": [5],
                "sort_spec": "",
            },
        }


class PatentSearchTool(BaseTool):
    name: str = "korean_patent_comprehensive_search"
    description: str = (
        "Search Korean patent database by technical keywords for patent information analysis. Use for patent landscape research, prior art analysis, and monitoring patent trends, including those of competitors, in Korean patents. Supports comprehensive search across multiple fields including title, abstract, claims, IPC classification, application numbers, dates, and more. Ideal for detailed patent research and analysis."
    )
    api: PatentSearchAPI = PatentSearchAPI()
    args_schema: t.Type[BaseModel] = PatentSearchArgs
    return_direct: bool = False

    def _run(
        self,
        word: str,
        patent: bool = True,
        utility: bool = True,
        lastvalue: str = "",
        page_no: int = 1,
        num_of_rows: int = 10,
        desc_sort: bool = True,
        sort_spec: str = "",
        **kwargs
    ) -> pd.DataFrame:
        if not word:
            if len(kwargs) == 0:
                raise ValueError("you must provide word or other search fields")

        result = self.api.search(
            word=word,
            patent=patent,
            utility=utility,
            lastvalue=lastvalue,
            page_no=page_no,
            num_of_rows=num_of_rows,
            desc_sort=desc_sort,
            sort_spec=sort_spec,
            **kwargs
        )
        return result
