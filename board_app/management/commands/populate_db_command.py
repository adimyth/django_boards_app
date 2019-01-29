from django.core.management.base import BaseCommand
from board_app.models import Board
from django.db import IntegrityError, DataError


class Command(BaseCommand):
    help = "Sub-command to populate database"

    @staticmethod
    def populate_board(name, description):
        Board.objects.create(name=name, description=description)

    def handle(self, *args, **options):
        try:
            self.populate_board('Reverse in Django', 'How to use reverse in django while testing')
        except IntegrityError:
            print(f"The entry already exists")
        except DataError:
            print(f"Board name exceeds the maximum limit")
