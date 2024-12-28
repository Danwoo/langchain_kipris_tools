from langchain_kipris_tools.kipris_api.foreign import ForeignPatentApplicantSearchAPI
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import typing as t
import pandas as pd
from langchain_kipris_tools.kipris_api.foreign.code import count_dict, sort_field_dict
from logging import getLogger

logger = getLogger(__name__)

class ForeignPatentApplicantSearchArgs(BaseModel):
    applicant: str = Field("", description="applicant, it must be filled, ")
    current_page: t.Optional[int] = Field(1, description="Current page number")
    sort_field: t.Optional[str] = Field("AD", description="Sort field")
    sort_state: t.Optional[bool] = Field(True, description="Sort state")
    collection_values: t.Optional[str] = Field("US", description="Collection values, default is US. other wise US, EP, WO, JP, PJ, CP, CN, TW, RU, CO, SE, ES, IL")
    
class ForeignPatentApplicantSearchTool(BaseTool):
    name:str = "foreign_patent_applicant_search"
    description:str = "foreign patent search by applicant"
    api:ForeignPatentApplicantSearchAPI = ForeignPatentApplicantSearchAPI()
    args_schema:t.Type[BaseModel] = ForeignPatentApplicantSearchArgs
    return_direct: bool = False

    def _run(self, applicant:str, 
             current_page:int=1,
             sort_field:str='AD',
             sort_state:bool=True,
             collection_values:str='US',
             **kwargs)->pd.DataFrame:
        if not applicant:    
            raise ValueError("international_open_number is required")
        if collection_values not in count_dict :
            raise ValueError(f"collection_values must be in {count_dict.keys()}")
        if sort_field not in sort_field_dict :
            raise ValueError(f"sort_field must be in {sort_field_dict.keys()}")
        logger.info(f"applicant: {applicant}")
        
        result = self.api.search(applicant=applicant, 
                                 current_page=current_page, 
                                 sort_field=sort_field, 
                                 sort_state=sort_state,
                                 collection_values=collection_values, **kwargs)
        return result
