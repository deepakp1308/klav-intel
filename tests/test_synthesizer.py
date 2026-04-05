"""Tests for the synthesis agent."""

from unittest.mock import MagicMock, patch

from agents.synthesizer import synthesize_brief, SYSTEM_PROMPT, BRIEF_TEMPLATE


def test_system_prompt_contains_key_rules():
    assert "Pyramid Principle" in SYSTEM_PROMPT
    assert "McKinsey" in SYSTEM_PROMPT
    assert "No filler phrases" in SYSTEM_PROMPT


def test_brief_template_has_all_sections():
    assert "EXECUTIVE SNAPSHOT" in BRIEF_TEMPLATE
    assert "PRODUCT & AI VELOCITY" in BRIEF_TEMPLATE
    assert "ANALYTICS & REPORTING POSITIONING" in BRIEF_TEMPLATE
    assert "GO-TO-MARKET & DIGITAL PRESENCE" in BRIEF_TEMPLATE
    assert "MARKET SIGNALS" in BRIEF_TEMPLATE
    assert "VOICE OF MARKET" in BRIEF_TEMPLATE
    assert "STRATEGIC IMPLICATIONS MATRIX" in BRIEF_TEMPLATE


@patch("agents.synthesizer.anthropic.Anthropic")
@patch("agents.synthesizer.ANTHROPIC_API_KEY", "test-key")
def test_synthesize_brief_returns_markdown(mock_anthropic_cls, sample_brief_markdown):
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text=sample_brief_markdown)]
    mock_message.usage = MagicMock(input_tokens=5000, output_tokens=2000)
    mock_client.messages.create.return_value = mock_message
    mock_anthropic_cls.return_value = mock_client

    result = synthesize_brief("test research", "April 4, 2026")
    assert "KLAV-INTEL" in result
    assert "EXECUTIVE SNAPSHOT" in result
    mock_client.messages.create.assert_called_once()


@patch("agents.synthesizer.anthropic.Anthropic")
@patch("agents.synthesizer.ANTHROPIC_API_KEY", "test-key")
def test_synthesize_uses_correct_model(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="# Brief")]
    mock_message.usage = MagicMock(input_tokens=100, output_tokens=100)
    mock_client.messages.create.return_value = mock_message
    mock_anthropic_cls.return_value = mock_client

    synthesize_brief("research", "April 4, 2026")

    call_kwargs = mock_client.messages.create.call_args.kwargs
    assert "claude" in call_kwargs["model"].lower() or "sonnet" in call_kwargs["model"].lower()
    assert call_kwargs["max_tokens"] > 4000
