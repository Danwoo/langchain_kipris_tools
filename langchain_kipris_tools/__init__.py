__version__ = '0.0.2'
from langchain_kipris_tools.kipris_tools import(
    KoreanPatentApplicantSearchTool, 
    KoreanPatentKeywordSearchTool, 
    KoreanPatentSearchTool, 
    KoreanPatentRighterSearchTool, 
    KoreanPatentApplicationNumberSearchTool,
    ForeignPatentFreeSearchTool,
    ForeignPatentInternationalApplicationNumberSearchTool,
    ForeignPatentInternationalOpenNumberSearchTool,
    ForeignPatentApplicantSearchTool,
    ForeignPatentApplicationNumberSearchTool,
    )       


import os
import typing as t
from langchain_core.tools import BaseTool

class LangChainKiprisKoreanTools:
    def set_api_key(self, api_key: str):    
        self.api_key = api_key
        os.environ['KIPRIS_API_KEY'] = api_key
    def get_tools(self) -> t.List[BaseTool]:
        tool_list = [KoreanPatentApplicantSearchTool(), KoreanPatentKeywordSearchTool(), KoreanPatentSearchTool(), KoreanPatentRighterSearchTool(), KoreanPatentApplicationNumberSearchTool()]
        return tool_list

class LangChainKiprisForeignTools:
    def set_api_key(self, api_key: str):
        self.api_key = api_key
        os.environ['KIPRIS_API_KEY'] = api_key
    def get_tools(self) -> t.List[BaseTool]:
        tool_list = [ForeignPatentFreeSearchTool(), ForeignPatentInternationalApplicationNumberSearchTool(), ForeignPatentInternationalOpenNumberSearchTool(), ForeignPatentApplicantSearchTool(), ForeignPatentApplicationNumberSearchTool()]
        return tool_list
