from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Product


# Create your tests here.

class ProductListCreateTest(APITestCase):
    def setUp(self):
        User.objects.create_user('admin', 'password')
        Token.objects.create(user=User.objects.get(username='admin'))

    def test_list(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__username='admin').key)
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        data = {
            'name': 'Test Product',
            'price': 10.00,
            'description': 'Test Description'
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__username='admin').key)
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, 201)

        data['price'] = -10.00
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, 400)

        data['price'] = 10.00
        data['name'] = 'a'
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, 400)

        data['name'] = 'Test Product'
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, 201)

        data['description'] = 'a'
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, 400)

        data['description'] = 'Test Description'
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, 201)

        self.client.logout()

        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, 401)


class ProductRetrieveUpdateDestroyTest(APITestCase):
    def setUp(self):
        User.objects.create_user('admin', 'password')
        Token.objects.create(user=User.objects.get(username='admin'))
        Product.objects.create(name='Test Product', price=10.00, description='Test Description')

    def test_retrieve(self):
        response = self.client.get('/api/products/1/')
        self.assertEqual(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__username='admin').key)
        response = self.client.get('/api/products/1/')
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        data = {
            'name': 'Test Product',
            'price': 10.00,
            'description': 'Test Description'
        }

        response = self.client.put('/api/products/1/', data)
        self.assertEqual(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__username='admin').key)
        response = self.client.put('/api/products/1/', data)
        self.assertEqual(response.status_code, 403)

        product = Product.objects.create(name='Best Product', price=10.00, description='Best Description', owner=User.objects.get(username='admin'))
        response = self.client.put('/api/products/2/', data)
        self.assertEqual(response.status_code, 200)

        data['price'] = -10.00
        response = self.client.put('/api/products/2/', data)
        self.assertEqual(response.status_code, 400)

        data['price'] = 10.00
        data['name'] = 'a'

        response = self.client.put('/api/products/2/', data)
        self.assertEqual(response.status_code, 400)

        data['name'] = 'Test Product'
        response = self.client.put('/api/products/2/', data)
        self.assertEqual(response.status_code, 200)

        data['description'] = 'a'
        response = self.client.put('/api/products/2/', data)
        self.assertEqual(response.status_code, 400)

        data['description'] = 'Test Description'
        response = self.client.put('/api/products/2/', data)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.put('/api/products/2/', data)
        self.assertEqual(response.status_code, 401)

    def test_destroy(self):
        response = self.client.delete('/api/products/1/')
        self.assertEqual(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__username='admin').key)
        response = self.client.delete('/api/products/1/')
        self.assertEqual(response.status_code, 403)

        product = Product.objects.create(name='Best Product', price=10.00, description='Best Description', owner=User.objects.get(username='admin'))
        response = self.client.delete('/api/products/2/')
        self.assertEqual(response.status_code, 204)

        response = self.client.delete('/api/products/2/')
        self.assertEqual(response.status_code, 404)

        self.client.logout()

        response = self.client.delete('/api/products/2/')
        self.assertEqual(response.status_code, 401)
