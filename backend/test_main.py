import unittest

from main import app


class AskTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_versioned_endpoint_and_compatibility_alias(self):
        for path in ("/api/v1/ask", "/ask"):
            with self.subTest(path=path):
                response = self.client.post(path, json={"question": "Next bus?"})
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.is_json)
                self.assertEqual(response.json, {
                    "answer": "The next bus is the 104, arriving in 5 minutes.",
                    "buses": [
                        {"route": "104", "stop": "Stamp Student Union", "arrives_in_min": 5},
                        {"route": "105", "stop": "Stamp Student Union", "arrives_in_min": 12},
                    ],
                })

    def test_omitted_question_and_extra_fields_remain_valid(self):
        for payload in ({}, {"question": "", "extra": True}):
            with self.subTest(payload=payload):
                response = self.client.post("/api/v1/ask", json=payload)
                self.assertEqual(response.status_code, 200)

    def test_invalid_payloads_return_shared_error(self):
        for payload in ([], "question", {"question": None}, {"question": 42}):
            with self.subTest(payload=payload):
                response = self.client.post("/api/v1/ask", json=payload)
                self.assertEqual(response.status_code, 400)
                self.assertTrue(response.is_json)
                self.assertEqual(set(response.json), {"error"})
                self.assertEqual(set(response.json["error"]), {"code", "message"})
                self.assertEqual(response.json["error"]["code"], "BAD_REQUEST")
                self.assertTrue(response.json["error"]["message"])

    def test_malformed_json(self):
        response = self.client.post(
            "/api/v1/ask", data="{", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"]["code"], "BAD_REQUEST")

    def test_non_json_request(self):
        response = self.client.post("/api/v1/ask", data="question=Next bus?")
        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.json["error"]["code"], "UNSUPPORTED_MEDIA_TYPE")

    def test_not_found(self):
        response = self.client.get("/api/v1/missing")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"]["code"], "NOT_FOUND")

    def test_method_not_allowed_preserves_allow_header(self):
        response = self.client.get("/api/v1/ask")
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json["error"]["code"], "METHOD_NOT_ALLOWED")
        self.assertIn("POST", response.headers["Allow"])


if __name__ == "__main__":
    unittest.main()
