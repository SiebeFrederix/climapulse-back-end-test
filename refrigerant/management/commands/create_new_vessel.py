from django.core.management.base import BaseCommand
from ...models import Vessel


class Command(BaseCommand):
    help = "Command for creating a new vessel."

    def add_arguments(self, parser):
        parser.add_argument("--vessel_name", type=str, required=True)
        parser.add_argument("--content", type=int, required=True)

    def handle(self, *args, **options):
        vessel = Vessel.objects.create(
            name=options["vessel_name"],
            content=options["content"]
        )

        self.stdout.write(
            f"Created new vessel ({vessel.name}) containing {vessel.content} kg"
        )
