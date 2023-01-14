import unittest
import requests


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5002/v1/subscribe"
    data = {"sub_level": 4, "expire_date": "2024", "api_key": "hfedj57755",
            "transaction_id": "de5cd79c571f18648c20ab7ec0959064b719e8516ec9734f861b3a9a48101e42"}
    header = {"user_id": "pooria"}

    def test_1(self):
        resp = requests.post(url=self.URL, json=self.data, headers=self.header)
        self.assertEqual(resp.status_code, 200)
        print('test 1 completed')


if __name__ == "__main__":
    tester = TestAPI()

    tester.test_1()
