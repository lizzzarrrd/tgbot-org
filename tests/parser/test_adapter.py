import requests_mock
from parser_module.adapters.llm_adapter import YandexGptAdapter

def test_adapter_complete_success():
    """Успешный запрос к API."""
    adapter = YandexGptAdapter("api_key", "gpt://uri")
    
    mock_resp = {
        "result": {
            "alternatives": [
                {"message": {"text": "merry christmas"}}
            ]
        }
    }

    with requests_mock.Mocker() as m:
        m.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion", json=mock_resp)
        
        result = adapter.complete("Prompt")
        
        assert result == "merry christmas"
        assert m.last_request.headers['Authorization'] == "Api-Key api_key"