from django.core.management.base import BaseCommand
from ...models import Vessel
from ...services import create_vessel, withdraw_from_vessel
import threading


class Command(BaseCommand):
    help = "Simulate condition when withdrawing refrigerant from a vessel."

    def handle(self, *args, **kwargs):
        # This will generate a new Vessel instance everytime the migrate command is ran
        create_vessel(name="Test vessel", content=50)
        self.stdout.write("Simulating condition...")
        self.run_simulation()

    def run_simulation(self):
        barrier = threading.Barrier(2)

        def user1():
            barrier.wait()
            # Only the first created Vessel is used in every withdraw prompt, hence id=1
            withdraw_from_vessel(vessel_id=1, amount=10)

        def user2():
            barrier.wait()
            withdraw_from_vessel(vessel_id=1, amount=10)

        t1 = threading.Thread(target=user1)
        t2 = threading.Thread(target=user2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        vessel = Vessel.objects.get(id=1)
        self.stdout.write(f"Remaining content: {vessel.content} kg")
