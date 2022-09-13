"""
Django commands to pause execution until database is available
"""

import time

from django.core.management.base import BaseCommand

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django custom command to pause execution until database is available"""

    def handle(self, *args, **options):
        # Help text to be displayed when running the command.
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])  # Check if database is available.
                db_up = True  # breaks the loop if database is available.
            except (
                Psycopg2OpError,
                OperationalError,
            ):  # If database is not available, wait 1 second and try again.
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)
        # Help text to be displayed when database is available.
        self.stdout.write(self.style.SUCCESS("Database available!"))
