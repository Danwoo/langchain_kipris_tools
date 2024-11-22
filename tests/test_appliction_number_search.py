import pytest
from langchain_kipris_tools.kipris_tools.application_number_search_tool import ApplicationNumberSearchTool
from langchain_kipris_tools.kipris_tools.application_number_search_tool import ApplicationNumberSearchArgs
@pytest.mark.skip(reason="not implemented")
def test_application_number_search():
    pass    

def test_application_number_search_args():
    params = ApplicationNumberSearchArgs(application_number="1020050050026")
    print(params)

def test_application_number_search_args_with_docs_start():
    params = ApplicationNumberSearchArgs(application_number="1020050050026", docs_start=10)
    print(params)

def test_application_number_search_args_with_docs_start_and_docs_count():
    params = ApplicationNumberSearchArgs(application_number="1020050050026", docs_start=10, docs_count=20)
    print(params)

def test_application_number_search_args_with_docs_start_and_docs_count_and_patent():
    params = ApplicationNumberSearchArgs(application_number="1020050050026", docs_start=10, docs_count=20, patent=True)
    print(params)

def test_application_number_search_class():
    search_tool = ApplicationNumberSearchTool()
    print(search_tool.args_schema)
    print(search_tool.name)
    print(search_tool.description)

def test_application_number_search_tool():
    search_tool = ApplicationNumberSearchTool()
    params = ApplicationNumberSearchArgs(application_number="1020050050026").model_dump()
    print(params)
    result = search_tool.run(tool_input=params)
    print(result)
    if result :
        assert True
    else:
        pytest.fail("result is empty")