from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.db import OperationalError


def test_wait_for_db_ready(capsys):
    # given
    test_command = "wait_for_db"

    # when
    call_command(test_command)

    # then
    captured = capsys.readouterr()
    assert "Waiting for database..." in captured.out
    assert "Database available!" in captured.out


@patch("time.sleep")
@patch("core.management.commands.wait_for_db.Command.check")
def test_db_not_available_in_first_attempts(
    mock_check: MagicMock, mock_sleep: MagicMock
):
    # given
    command = "wait_for_db"
    mock_check.side_effect = [OperationalError] * 2 + [MagicMock]

    # when
    call_command(command)

    # then
    assert mock_sleep.call_count == 2
