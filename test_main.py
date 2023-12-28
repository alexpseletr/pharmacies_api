import unittest
from fastapi.testclient import TestClient
from main import app  

class TestApi(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.api_key = "chave_de_api_fixa"
        self.auth_token = "token_de_autorizacao_fixo"

    def test_list_patients(self):
        response = self.client.get(
            "/patients",
            headers={"Api-Key": self.api_key, "Authorization": f"Bearer {self.auth_token}"}
        )
        self.assertEqual(response.status_code, 200)

    def test_list_pharmacies(self):
        response = self.client.get(
            "/pharmacies",
            headers={"Api-Key": self.api_key, "Authorization": f"Bearer {self.auth_token}"}
        )
        self.assertEqual(response.status_code, 200)

    def test_list_transactions(self):
        response = self.client.get(
            "/transactions",
            headers={"Api-Key": self.api_key, "Authorization": f"Bearer {self.auth_token}"}
        )
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
