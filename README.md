# langchain_kipris_tools

plus.kipris.or.kr 에서 제공하는 api_key를 이용하여 특허를 검색하는 langchain tool 구현체입니다.
api_key는 본인의 키를 사용해야 합니다.
가입은 [link](plus.kipris.or.kr/portal/main.do) 에서 가입 후 사용 가능합니다.

사용 예제

```python
import os
os.environ["KIPRIS_API_KEY"] = ''

from langchain_kipris_tools import LangChainKiprisKoreanTools
kipristools = LangChainKiprisKoreanTools()
tools = kipristools.get_tools()
```

제공하는 api 목록

| 순번 |국가| api 명칭                     | 설명                | 참조 url                                                                                                                                                                                 |
| ---- | ----|------------------------ | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | 한국| patent_search_tool           | 특허 전체 검색      | [link](https://plus.kipris.or.kr/portal/popup/DBII_000000000000001/SC002/ADI_0000000000002944/apiDescriptionSearch.do)                                                                      |
| 2    | 한국| patent_keyword_search_tool   | 특허 키워드 검색    | [link](https://plus.kipris.or.kr/portal/popup/DBII_000000000000001/SC002/ADI_0000000000010162/apiDescriptionSearch.do)                                                                      |
| 3    | 한국| patent_applicant_search_tool | 특허 출원인 검색    | [link](https://plus.kipris.or.kr/portal/popup/DBII_000000000000001/SC002/ADI_0000000000015118/apiDescriptionSearch.do)                                                                      |
| 4    | 한국| patent_righter_search_tool   | 특허 권리자 검색    | [link](https://plus.kipris.or.kr/portal/data/service/DBII_000000000000001/view.do?menuNo=200100&kppBCode=&kppMCode=&kppSCode=&subTab=SC001&entYn=N&clasKeyword=#soap_ADI_0000000000015121)  |
| 5    | 한국| patent_number_search_tool    | 특허 출원 번호 검색 | [link](https://plus.kipris.or.kr/portal/data/service/DBII_000000000000001/view.do?menuNo=200100&kppBCode=&kppMCode=&kppSCode=&subTab=SC001&entYn=N&clasKeyword=#soap_ADI_0000000000010163)  |

# Example

```python
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# 본인의 kipris api key가 KIPRIS_API_KEY 환경변수에 저장되어 있어야 합니다.
# os.environ["KIPRIS_API_KEY"]='사용자 발급 api key'
from langchain_openai import ChatOpenAI
from langchain_kipris_tools import LangChainKiprisKoreanTools


load_dotenv()
tool_class = LangChainKiprisKoreanTools()
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
        selected_tool = {
            "applicant_search": tools[0], 
            "patent_keyword_search": tools[1], 
            "patent_search":tools[2],
            "application_number_search":tools[3],
            "righter_search":tools[4]
            }[tool_call["name"].lower()]
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

실제 사용 예제 
![image](assets/usage.png)

변경 내역 

- 2024-12-25 
    - 패키지 의존성 변경
        - Langgraph 의존성 추가
        - Redis 의존성 추가
    - Langgraph의 graph에서 사용할 Node Template 추가
    - Langgraph의 checkpoint 추가
        - Redis 사용
        - 원본 : [link](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/how-tos/persistence_redis.ipynb)
    - Kipris tool 패키지 구조 변경 내역 코드 반영.
        - LangchainKiprisKoreanTools 명칭 변경
        - LangchainKiprisTools -> LangchainKiprisKoreanTools 명칭 변경
    - 예제 코드 수정 
        패키지/클래스 변경에 따른 변경. 


- 2024-11-23
    - 한국 및 해외 검색 도구 추가를 위한 구조 변경
    - 특허 검색 API 추가
        - 권리자 검색
        - 출원번호 검색

- 2024-11-11
    - 테스트 코드 추가 
    - 예제 코드 추가 
    - 아규먼트 처리 로직 수정


- 2024-11-10
    - 최초 작성
