import os

from dotenv import load_dotenv
load_dotenv()

# 본인의 kipris api key가 KIPRIS_API_KEY 환경변수에 저장되어 있어야 합니다.
# os.environ["KIPRIS_API_KEY"]='사용자 발급 api key'
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticToolsParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from langchain_kipris_tools import LangChainKiprisTools
from langchain_kipris_tools.kipris_tools.patent_search_tool import PatentSearchArgs

tool_class = LangChainKiprisTools()
kipris_tools = tool_class.get_tools()
llm = ChatOpenAI(model="gpt-4o-mini")

def call_with_tool(query, tools):
    from datetime import datetime as dt
    start = dt.now()

    llm_with_tools = llm.bind_tools(tools)
    chain = llm_with_tools 
    messages = [HumanMessage(query)]
    ai_msg = chain.invoke(messages)
    messages.append(ai_msg)

    for tool_call in ai_msg.tool_calls:
        selected_tool = {"applicant_search": tools[0], "patent_keyword_search": tools[1], "patent_search":tools[2]}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        print(f'call {selected_tool.name}')
        print(tool_call)
        messages.append(tool_msg)
    result = llm_with_tools.invoke(messages).content
    duration = dt.now() - start
    print(f'duration:{duration}')
    return result

result = call_with_tool("최신 특허중 현대자동차 특허 10개를 표시해줘, 표시항목에 출원인도 포함해서 보여줘", kipris_tools)