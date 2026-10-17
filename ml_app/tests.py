from django.test import TestCase
from django.urls import reverse

VALID = {"total_bill": "20", "sex": "Male", "smoker": "No", "day": "Sun", "time": "Dinner", "size": "2"}


class PredictTests(TestCase):
    def test_home_page_loads(self):
        self.assertEqual(self.client.get(reverse("index")).status_code, 200)

    def test_valid_prediction(self):
        res = self.client.post(reverse("predict"), VALID)
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertTrue(body["ok"])
        # Notebook check: [20, Male, No, Sun, Dinner, 2] -> about 3.09
        self.assertAlmostEqual(body["tip"], 3.09, places=1)

    def test_invalid_input_is_rejected(self):
        res = self.client.post(reverse("predict"), {**VALID, "size": "0"})
        self.assertEqual(res.status_code, 400)
        self.assertIn("size", res.json()["errors"])

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(reverse("predict")).status_code, 405)
