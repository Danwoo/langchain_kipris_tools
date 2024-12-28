import os

from dotenv import load_dotenv
load_dotenv()
import traceback
# 본인의 kipris api key가 KIPRIS_API_KEY 환경변수에 저장되어 있어야 합니다.
# os.environ["KIPRIS_API_KEY"]='사용자 발급 api key'
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticToolsParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain_core.messages import ToolMessage
from langchain_kipris_tools import LangChainKiprisForeignTools

tool_class = LangChainKiprisForeignTools()
kipris_tools = tool_class.get_tools()
llm = ChatOpenAI(model="gpt-4o-mini")

def call_with_tool(query, tools):   
    from datetime import datetime as dt
    start = dt.now()

    llm_with_tools = llm.bind_tools(tools)
    messages = [HumanMessage(content=query)]
    ai_msg = llm_with_tools.invoke(messages)
    
    # tool_calls가 있는 경우에만 처리
    if hasattr(ai_msg, 'tool_calls') and ai_msg.tool_calls:
        # 먼저 assistant 메시지 추가
        messages.append(ai_msg)
        
        # 각 tool 호출에 대한 응답 처리
        for tool_call in ai_msg.tool_calls:
            tool_name = tool_call['name']
            print(f"tool_name: {tool_name}")
            try:
                tools_dict = {tool.name.lower(): tool for tool in tools}
                tool_name = tool_call['name'].lower()
                
                if tool_name not in tools_dict:
                    print(f"경고: '{tool_name}' 도구를 찾을 수 없습니다.")
                    # 도구를 찾을 수 없는 경우에도 빈 응답 추가
                    messages.append(ToolMessage(
                        tool_call_id=tool_call['id'],
                        content="도구를 찾을 수 없습니다.",
                        name=tool_name
                    ))
                    continue
                
                selected_tool = tools_dict[tool_name]
                print(f"selected_tool: {selected_tool}")
                tool_result = selected_tool.invoke(tool_call)
                
                # 반드시 각 tool_call에 대한 응답 추가
                messages.append(ToolMessage(
                    tool_call_id=tool_call['id'],
                    content=str(tool_result),
                    name=tool_name
                ))
                
            except Exception as e:
                print(f"도구 실행 중 오류 발생: {str(e)}")
                print(traceback.format_exc())
                # 오류 발생시에도 응답 추가
                messages.append(ToolMessage(
                    tool_call_id=tool_call['id'],
                    content=f"오류 발생: {str(e)}",
                    name=tool_name
                ))
        
        # 모든 tool 응답을 처리한 후 최종 응답 생성
        final_response = llm_with_tools.invoke(messages)
        duration = dt.now() - start
        print(f'duration:{duration}')
        return final_response.content
    
    duration = dt.now() - start
    print(f'duration:{duration}')
    return ai_msg.content

result = call_with_tool("최신 특허중 현대자동차 특허 10개를 표시해줘, 표시항목에 출원인도 포함해서 보여줘", kipris_tools)
print(result)