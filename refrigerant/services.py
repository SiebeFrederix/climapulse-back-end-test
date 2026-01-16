from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Vessel


def create_vessel(name: str, content: int) -> Vessel:
    if content < 0:
        raise ValidationError("Content must be non-negative")

    return Vessel.objects.create(name=name, content=content)

def withdraw_from_vessel(vessel_id, amount):
    # Use row locking fix race condition bug
    with transaction.atomic():
        try:
            vessel = (
                Vessel.objects
                .select_for_update()
                .get(id=vessel_id)
            )
        except Vessel.DoesNotExist:
            raise ValidationError("Vessel does not exist")

        if vessel.content == 0:
            raise ValidationError("Vessel is empty")

        if vessel.content < amount:
            raise ValidationError(
                f"Only {vessel.content} kg left in vessel"
            )

        vessel.content -= amount
        vessel.save()
