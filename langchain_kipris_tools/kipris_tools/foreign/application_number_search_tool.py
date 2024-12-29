from langchain_kipris_tools.kipris_api.foreign import ForeignPatentApplicationNumberSearchAPI
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import typing as t
import pandas as pd
from langchain_kipris_tools.kipris_api.foreign.code import count_dict, sort_field_dict

class ForeignPatentApplicationNumberSearchArgs(BaseModel):
    application_number: str = Field("", description="application number, it must be filled")
    current_page: t.Optional[int] = Field(1, description="Current page number")
    sort_field: t.Optional[str] = Field("AD", description="Sort field")
    sort_state: t.Optional[bool] = Field(True, description="Sort state")
    collection_values: t.Optional[str] = Field("US", description="Collection values, default is US. other wise US, EP, WO, JP, PJ, CP, CN, TW, RU, CO, SE, ES, IL")
    
class ForeignPatentApplicationNumberSearchTool(BaseTool):
    name:str = "foreign_patent_application_number_search"
    description:str = "foreign patent search by application number, this tool is for foreign(US, EP, WO, JP, PJ, CP, CN, TW, RU, CO, SE, ES, IL) patent search"
    api:ForeignPatentApplicationNumberSearchAPI = ForeignPatentApplicationNumberSearchAPI()
    args_schema:t.Type[BaseModel] = ForeignPatentApplicationNumberSearchArgs
    return_direct: bool = False

    def _run(self, application_number:str, 
             current_page:int=1,
             sort_field:str='AD',
             sort_state:bool=True,
             collection_values:str='US',
             **kwargs)->pd.DataFrame:
        if not application_number:    
            raise ValueError("application_number is required")
        if collection_values not in count_dict :
            raise ValueError(f"collection_values must be in {count_dict.keys()}")
        if sort_field not in sort_field_dict :
            raise ValueError(f"sort_field must be in {sort_field_dict.keys()}")
        result = self.api.search(application_number=application_number, 
                                 current_page=current_page, 
                                 sort_field=sort_field, 
                                 sort_state=sort_state,
                                 collection_values=collection_values, **kwargs)
        return result
