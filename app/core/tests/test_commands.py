"""
Test the custom command module.
"""

from unittest.mock import patch  # mock the behavior of the db

from psycopg2 import OperationalError as Psycopg2OpError  # error

from django.core.management import call_command  # helper funtion to call the command

from django.db.utils import OperationalError  # error

from django.test import SimpleTestCase  # base test class to create and test unittest


@patch(
    "core.management.commands.wait_for_db.Command.check"
)  # mock the behavior of the db.
class CommandTest(SimpleTestCase):
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db when db is available"""
        patched_check.return_value = True
        # call the command wait for db
        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_checK):
        """Test waiting for db when operational error is raised"""
        patched_checK.side_effect = (
            [Psycopg2OpError] * 2 + [OperationalError] * 3 + [True]
        )

        call_command("wait_for_db")

        self.assertEqual(patched_checK.call_count, 6)
        patched_checK.assert_called_with(databases=["default"])
