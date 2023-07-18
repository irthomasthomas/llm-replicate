from click.testing import CliRunner
import json
from llm.cli import cli
import pathlib
import pytest
from unittest.mock import Mock, patch
import replicate

flan_t5 = json.loads(
    (pathlib.Path(__file__).parent / "replicate-flan-t5-xl.json").read_text()
)


@patch("replicate.Client")
def test_replicate_prompt(mock_class, user_path):
    runner = CliRunner()

    mock_client = Mock()
    mock_run_output = ["hello", " world"]
    mock_client.run.return_value = mock_run_output
    mock_class.return_value = mock_client

    (user_path / "replicate").mkdir()
    true, false, null = True, False, None
    (user_path / "replicate" / "fetch-models.json").write_text(
        json.dumps([flan_t5]),
        "utf-8",
    )
    result = runner.invoke(cli, ["-m", "replicate-flan-t5-xl", "say hi"])
    assert result.exit_code == 0, result.output
    assert result.output == "hello world\n"
