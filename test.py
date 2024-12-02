import unittest
import json
from app import app
from data import data


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Очистка списка перед каждым тестом
        data["items"] = []

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to the API!', response.get_data(as_text=True))

    def test_get_items(self):
        response = self.app.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_add_item(self):
        response = self.app.post('/items', json={"item": "Test Item"})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Test Item', response.json["item"])

    def test_delete_item(self):
        # Add an item first
        self.app.post('/items', json={"item": "To be deleted"})
        # Delete the item
        response = self.app.delete('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Item deleted")  # Проверяем сообщение

    def test_delete_item_out_of_range(self):
        response = self.app.delete('/items/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Index out of range', response.json["error"])

if __name__ == '__main__':
    unittest.main()
