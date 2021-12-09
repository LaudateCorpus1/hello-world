import unittest
import time

from main import app, data, route_default, route_health, route_slow, route_bad, main

class TestApp(unittest.TestCase):

    def test_data(self):
        self.assertEqual(data(), 'Hello world')

    def test_route_default(self):
        with app.test_client() as client:
            res = client.get('/')
            self.assertIsInstance(res, app.response_class)
            self.assertEqual(res.status_code, 200)
    
    def test_route_bad(self):
        with app.test_client() as client:
            res = client.get('/bad')
            self.assertIsInstance(res, app.response_class)
            self.assertEqual(res.status_code, 500)
    
    def test_route_slow(self):
        with app.test_client() as client:
            res = client.get('/slow')
            self.assertIsInstance(res, app.response_class)
            self.assertEqual(res.status_code, 200)

    def test_route_health(self):
        with app.test_client() as client:
            res = client.get('/health')
            self.assertIsInstance(res, app.response_class)
            self.assertEqual(res.status_code, 200)
    
    def test_main(self):
        self.assertLogs(main())

if __name__ == '__main__':
    unittest.main()