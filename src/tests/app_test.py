import unittest
from app import app, store
from varasto import Varasto


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        store.warehouses.clear()
        store.next_id = 1

    def test_index_empty(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouses', response.data)
        self.assertIn(b'No warehouses yet', response.data)

    def test_create_warehouse_get(self):
        response = self.app.get('/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create New Warehouse', response.data)

    def test_create_warehouse_post(self):
        response = self.app.post('/create', data={
            'name': 'Test Warehouse',
            'capacity': '100',
            'initial': '50'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Warehouse', response.data)
        self.assertEqual(len(store.warehouses), 1)
        warehouse = store.get(1)
        self.assertEqual(warehouse['name'], 'Test Warehouse')
        self.assertAlmostEqual(warehouse['varasto'].tilavuus, 100)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 50)

    def test_create_warehouse_empty_name(self):
        response = self.app.post('/create', data={
            'name': '',
            'capacity': '100',
            'initial': '0'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Name is required', response.data)
        self.assertEqual(len(store.warehouses), 0)

    def test_view_warehouse(self):
        store.add('Test Warehouse', Varasto(100, 50))
        response = self.app.get('/warehouse/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Warehouse', response.data)
        self.assertIn(b'50', response.data)

    def test_view_nonexistent_warehouse(self):
        response = self.app.get('/warehouse/999', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_add_to_warehouse(self):
        store.add('Test Warehouse', Varasto(100, 50))
        response = self.app.post('/warehouse/1/add', data={
            'amount': '25'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        warehouse = store.get(1)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 75)

    def test_remove_from_warehouse(self):
        store.add('Test Warehouse', Varasto(100, 50))
        response = self.app.post('/warehouse/1/remove', data={
            'amount': '20'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        warehouse = store.get(1)
        self.assertAlmostEqual(warehouse['varasto'].saldo, 30)

    def test_edit_warehouse_get(self):
        store.add('Test Warehouse', Varasto(100, 50))
        response = self.app.get('/warehouse/1/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Warehouse', response.data)
        self.assertIn(b'Test Warehouse', response.data)

    def test_edit_warehouse_post(self):
        store.add('Test Warehouse', Varasto(100, 50))
        response = self.app.post('/warehouse/1/edit', data={
            'name': 'Updated Warehouse'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        warehouse = store.get(1)
        self.assertEqual(warehouse['name'], 'Updated Warehouse')

    def test_delete_warehouse(self):
        store.add('Test Warehouse', Varasto(100, 50))
        response = self.app.post(
            '/warehouse/1/delete',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(store.warehouses), 0)

    def test_multiple_warehouses(self):
        store.add('Warehouse 1', Varasto(100, 10))
        store.add('Warehouse 2', Varasto(200, 20))
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse 1', response.data)
        self.assertIn(b'Warehouse 2', response.data)

    def test_add_nonexistent_warehouse(self):
        response = self.app.post(
            '/warehouse/999/add',
            data={'amount': '10'},
            follow_redirects=False
        )
        self.assertEqual(response.status_code, 302)

    def test_remove_nonexistent_warehouse(self):
        response = self.app.post(
            '/warehouse/999/remove',
            data={'amount': '10'},
            follow_redirects=False
        )
        self.assertEqual(response.status_code, 302)

    def test_edit_nonexistent_warehouse(self):
        response = self.app.get('/warehouse/999/edit', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
