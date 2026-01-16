from django.core.management.base import BaseCommand, CommandError
from ...services import withdraw_from_vessel


class Command(BaseCommand):
    help = "Command for withdrawing refrigerant from a vessel."

    def add_arguments(self, parser):
        parser.add_argument("--vessel_id", type=int, required=True)
        parser.add_argument("--amount", type=int, required=True)

    def handle(self, *args, **options):
        try:
            vessel = withdraw_from_vessel(
                vessel_id=options["vessel_id"],
                amount=options["amount"]
            )
        except Exception as e:
            raise CommandError(str(e))

        self.stdout.write(
            f"{vessel.content} kg remaining in {vessel.name}"
        )
