import pytest
from langchain_kipris_tools.kipris_tools.righter_search_tool import RighterSearchTool
from langchain_kipris_tools.kipris_tools.righter_search_tool import RighterSearchArgs
@pytest.mark.skip(reason="not implemented")
def test_applicant_search():
    pass

def test_righter_search_args():
    params = RighterSearchArgs(righter="삼성전자")
    print(params)

def test_righter_search_args_with_docs_start():
    params = RighterSearchArgs(righter="삼성전자", docs_start=10)
    print(params)

def test_righter_search_args_with_docs_start_and_docs_count():
    params = RighterSearchArgs(righter="삼성전자", docs_start=10, docs_count=20)
    print(params)

def test_righter_search_args_with_docs_start_and_docs_count_and_patent():
    params = RighterSearchArgs(righter="삼성전자", docs_start=10, docs_count=20, patent=True)
    print(params)

def test_righter_search_class():
    search_tool = RighterSearchTool()
    print(search_tool.args_schema)
    print(search_tool.name)
    print(search_tool.description)

def test_righter_search_tool():
    search_tool = RighterSearchTool()
    params = RighterSearchArgs(righter="삼성전자").model_dump()
    print(params)
    result = search_tool.run(tool_input=params)
    print(result)
    if result :
        assert True
    else:
        pytest.fail("result is empty")