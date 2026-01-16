from django.core.management.base import BaseCommand
from ...models import Vessel
from ...services import withdraw_from_vessel
import threading


class Command(BaseCommand):
    help = "Simulate race condition when concurrently withdrawing refrigerant from a vessel."

    def add_arguments(self, parser):
        # Flag for restarting simulation
        parser.add_argument(
            "--restart",
            action="store_true",
            help="Reset vessel content to initial state before simulation",
        )

    def handle(self, *args, **options):
        vessel, created = Vessel.objects.get_or_create(
            name="Test vessel",
            defaults={"content": 50}
        )

        if options["restart"]:
            vessel.content = 50
            vessel.save()

        if created:
            self.stdout.write("Created Test vessel")

        if options["restart"]:
            vessel.content = 50
            vessel.save()
            self.stdout.write("Reinitialized Test vessel")


        self.stdout.write("Simulating concurrent withdraw...")
        self.run_simulation(vessel_id=vessel.id)

    def run_simulation(self, vessel_id):
        barrier = threading.Barrier(2)

        def user():
            barrier.wait()
            try:
                withdraw_from_vessel(vessel_id=vessel_id, amount=10)
            except Exception as e:
                self.stdout.write(str(e))

        t1 = threading.Thread(target=user)
        t2 = threading.Thread(target=user)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        vessel = Vessel.objects.get(id=vessel_id)
        self.stdout.write(f"Remaining content: {vessel.content} kg")
