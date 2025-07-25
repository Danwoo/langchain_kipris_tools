from langchain_kipris_tools.kipris_api.foreign import ForeignPatentFreeSearchAPI
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import typing as t
import pandas as pd
from langchain_kipris_tools.kipris_api.foreign.code import count_dict, sort_field_dict

class ForeignPatentFreeSearchArgs(BaseModel):
    free: str = Field("", description="Search query, if query has whitespace then transform to web encoding. default is an empty string. this value should be english or collection_values's value if this is empty, then i should ask user to input query.")
    current_page: t.Optional[int] = Field(1, description="Current page number")
    sort_field: t.Optional[str] = Field("AD", description="Sorting option\n- 'AD': Sort by application date (출원일자) - for latest applications\n- 'GD': Sort by registration date (등록일자) - for latest registrations\n- 'PD': Sort by publication date (공고일자) - for latest publications\n- 'OPD': Sort by open date (공개일자) - for latest disclosures")
    sort_state: t.Optional[bool] = Field(True, description="Sort state(True or False)")
    collection_values: t.Optional[str] = Field("US", description="Collection value. Must be one of the following: [US, EP, WO, JP, PJ, CP, CN, TW, RU, CO, SE, ES, IL]. If not specified, the default is US.Exactly one value must be selected.")
    
class ForeignPatentFreeSearchTool(BaseTool):
    name:str = "foreign_patent_free_search"
    description:str = "foreign patent search by user input keyword, this tool is for foreign(US, EP, WO, JP, PJ, CP, CN, TW, RU, CO, SE, ES, IL) patent search"
    api:ForeignPatentFreeSearchAPI = ForeignPatentFreeSearchAPI()
    args_schema:t.Type[BaseModel] = ForeignPatentFreeSearchArgs
    return_direct: bool = False

    def _run(self, free:str, 
             current_page:int=1,
             sort_field:str='AD',
             sort_state:bool=True,
             collection_values:str='US',
             **kwargs)->pd.DataFrame:
        if not free:
            raise ValueError("free is required")
        if collection_values not in count_dict :
            raise ValueError(f"collection_values must be in {count_dict.keys()}")
        if sort_field not in sort_field_dict :
            raise ValueError(f"sort_field must be in {sort_field_dict.keys()}")
        result = self.api.search(free=free, 
                                 current_page=current_page, 
                                 sort_field=sort_field, 
                                 sort_state=sort_state,
                                 collection_values=collection_values, **kwargs)
        return result
