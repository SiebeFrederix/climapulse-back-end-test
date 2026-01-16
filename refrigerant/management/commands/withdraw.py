from django.core.management.base import BaseCommand
from django.db.models import F
from ...models import Vessel
import threading


class Command(BaseCommand):
    help = "Simulate condition when withdrawing refrigerant from a vessel."

    def handle(self, *args, **kwargs):
        # This will generate a new Vessel instance everytime the migrate command is ran
        Vessel.objects.create(name="Test Vessel", content=50.0)
        self.stdout.write("Simulating condition...")
        self.run_simulation()

    def run_simulation(self):
        barrier = threading.Barrier(2)

        def user1():
            barrier.wait()
            # Only the first created Vessel is used in every withdraw prompt, hence id=1
            vessel = Vessel.objects.filter(id=1)
            # F expression performs an actual SQL operation on the database
            # It does not load the data into a local python variable first
            vessel.update(content=F("content") - 10)

        def user2():
            barrier.wait()
            vessel = Vessel.objects.filter(id=1)
            vessel.update(content=F("content") - 10)

        t1 = threading.Thread(target=user1)
        t2 = threading.Thread(target=user2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        vessel = Vessel.objects.get(id=1)
        self.stdout.write(f"Remaining content: {vessel.content} kg")
