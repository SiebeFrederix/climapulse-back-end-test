from django.test import TestCase
from django.core.exceptions import ValidationError
from refrigerant.models import Vessel
from refrigerant.services import withdraw_from_vessel

class WithdrawFromVesselTests(TestCase):
    def setUp(self):
        self.vessel = Vessel.objects.create(
            name="Test Vessel",
            content=50
        )

    def test_withdraw_reduces_content(self):
        withdraw_from_vessel(
            vessel_id=self.vessel.id,
            amount=10
        )

        self.vessel.refresh_from_db()
        self.assertEqual(self.vessel.content, 40)

    def test_withdraw_more_than_available_raises_error(self):
        with self.assertRaises(ValidationError):
            withdraw_from_vessel(
                vessel_id=self.vessel.id,
                amount=60
            )

        self.vessel.refresh_from_db()
        self.assertEqual(self.vessel.content, 50)
