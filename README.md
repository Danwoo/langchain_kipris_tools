# langchain_kipris_tools

plus.kipris.or.kr 에서 제공하는 api_key를 이용하여 특허를 검색하는 langchain tool 구현체입니다.
api_key는 본인의 키를 사용해야 합니다.
가입은 plus.kipris.or.kr/portal/main.do 에서 가입 후 사용 가능합니다.

사용 예제

```python
import os
os.environ["KIPRIS_API_KEY"] = ''

from langchain_kipris_tools import LangChainKiprisTools
kipristools = LangChainKiprisTools()
tools = kipristools.get_tools()
```

제공하는 api 목록

| 순번 | api 명칭                     | 설명             | 참조 url                                                                                                            |
| ---- | ---------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------- |
| 1    | patent_search_tool           | 특허 전체 검색   | [link](https://plus.kipris.or.kr/portal/popup/DBII_000000000000001/SC002/ADI_0000000000002944/apiDescriptionSearch.do) |
| 2    | patent_keyword_search_tool   | 특허 키워드 검색 | [link](https://plus.kipris.or.kr/portal/popup/DBII_000000000000001/SC002/ADI_0000000000010162/apiDescriptionSearch.do) |
| 3    | patent_applicant_search_tool | 특허 출원인 검색 | [link](https://plus.kipris.or.kr/portal/popup/DBII_000000000000001/SC002/ADI_0000000000015118/apiDescriptionSearch.do) |


# Example

```python
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# 본인의 kipris api key가 KIPRIS_API_KEY 환경변수에 저장되어 있어야 합니다.
# os.environ["KIPRIS_API_KEY"]='사용자 발급 api key'
from langchain_openai import ChatOpenAI
from langchain_kipris_tools import LangChainKiprisTools


load_dotenv()
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
```
