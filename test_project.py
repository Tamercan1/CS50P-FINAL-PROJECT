from unittest.mock import MagicMock, patch
from project import decide_mode, build_contents, get_persona_prompt


PERSONALITIES = [
    {
        "id": "normal",
        "prompt": {
            "display_name": "Normal",
            "system_prompt": "Be friendly",
            "personality": "casual",
            "greeting": "Hey!"
        }
    },
    {
        "id": "programmer",
        "prompt": {
            "display_name": "Senior Programmer",
            "system_prompt": "Help with code",
            "personality": "technical",
            "greeting": "Let's code!"
        }
    }
]


@patch("project.client")
def test_decide_mode(mock_client):
    mock_response = MagicMock()

    mock_response.text = '{"switch": true, "mode": "programmer"}'
    mock_client.models.generate_content.return_value = mock_response
    result = decide_mode("switch to programmer mode", PERSONALITIES)
    assert result["switch"] is True
    assert result["mode"] == "programmer"

    mock_response.text = '{"switch": true, "mode": "einstein"}'
    mock_client.models.generate_content.return_value = mock_response
    result = decide_mode("act like einstein", PERSONALITIES)
    assert result["switch"] is True
    assert result["mode"] == "einstein"

    mock_response.text = '{"switch": false}'
    result = decide_mode("what is the weather today?", PERSONALITIES)
    assert result["switch"] is False


def test_build_contents():
    result = build_contents("list me chicken adobo recipe", [])
    assert result[-1].role == "user"
    assert result[-1].parts[0].text == "list me chicken adobo recipe"
    assert len(result) == 1

    existing = build_contents("hi", [])
    result = build_contents("bye", existing)
    assert result[-1].parts[0].text == "bye"
    assert result[0].parts[0].text == "hi"
    assert len(result) == 2


def test_get_persona_prompt():
    
    result = get_persona_prompt("programmer", PERSONALITIES)
    assert result["display_name"] == "Senior Programmer"
    assert result["system_prompt"] == "Help with code"
    assert result["personality"] == "technical"
    assert result["greeting"] == "Let's code!"

    result = get_persona_prompt("normal", PERSONALITIES)
    assert result["display_name"] == "Normal"
    assert result["system_prompt"] == "Be friendly"
    assert result["personality"] == "casual"
    assert result["greeting"] == "Hey!"

    result = get_persona_prompt("normal", [])
    assert result is None