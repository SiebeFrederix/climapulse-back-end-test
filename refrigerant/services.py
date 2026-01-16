from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Vessel


def withdraw_from_vessel(vessel_id, amount):
    # Use row locking to fix race condition bug
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
                f"Only {vessel.content} kg left in vessel, tried to withdraw {amount} kg"
            )

        vessel.content -= amount
        vessel.save()

        return vessel
