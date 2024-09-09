from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Property, Device

class UserFlowTestCase(TestCase):
    def setUp(self):
        print("Setting up the test environment...")
        # Creating a test user
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'Passw0rd!2024'  # Updated password to follow the pattern

        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
        print(f"Test user created: {self.username}")

    def test_create_account(self):
        print("Starting account creation test...")
        response = self.client.post(reverse('signup'), {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'uniqueuser',
            'email': 'uniqueuser@example.com',
            'password': 'Passw0rd!2024',  # Updated password
            'confirm_password': 'Passw0rd!2024',  # Confirmed password
        })
        print(f"Server response: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_login(self):
        print("Starting login test...")
        self.client.post(reverse('signup'), {
            'first_name': 'Test',
            'last_name': 'User',
            'username': self.username,
            'email': self.email,
            'password': 'Passw0rd!2024',  # Updated password
            'confirm_password': 'Passw0rd!2024',  # Confirmed password
        })
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': 'Passw0rd!2024',  # Updated password
        })
        print(f"Login response: {response.status_code}")
        print(f"Login content: {response.content.decode()}")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_create_property(self):
        print("Starting property creation test...")
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('add_property'), {
            'name': 'Test Property',
            'description': 'This is a test property.',
            'latitude': 123.456,
            'longitude': 78.910,
        })
        print(f"Property creation response: {response.status_code}")
        print(f"Property response content: {response.content.decode()}")
        self.assertEqual(response.status_code, 302)
        
        # Ensure that the property was created
        self.property_id = Property.objects.get(name='Test Property').id
        print(f"Created property ID: {self.property_id}")

    def test_edit_property(self):
        print("Starting property editing test...")
        self.client.login(username=self.username, password=self.password)
        if not hasattr(self, 'property_id'):
            print("Property not found. Creating a new property...")
            self.test_create_property()  # Ensure property exists

        response = self.client.post(reverse('edit_property', args=[self.property_id]), {
            'name': 'Updated Property',
            'description': 'Updated description.',
            'latitude': 123.456,
            'longitude': 78.910,
        })
        print(f"Property edit response: {response.status_code}")
        print(f"Property edit response content: {response.content.decode()}")
        self.assertEqual(response.status_code, 302)

    def test_add_devices(self):
        print("Starting device addition test...")
        self.client.login(username=self.username, password=self.password)
        property = Property.objects.create(
            user=self.user,
            name='Test Property for Devices',
            description='Property for device tests.',
            latitude=123.456,
            longitude=78.910,
        )

        device_types = ['Sprinkler', 'Tank', 'Thermometer', 'Hygrometer', 'Camera']
        device_names = ['Sprinkler Device', 'Tank Device', 'Thermometer Device', 'Hygrometer Device', 'Camera Device']

        for device_type, device_name in zip(device_types, device_names):
            print(f"Adding device {device_name} of type {device_type}...")
            response = self.client.post(reverse('add_device', args=[property.id]), {
                'type': device_type,
                'name': device_name,
                'key': 'T3ST3-T3ST3-T3ST3',
                'status': 'Off',
            })
            print(f"Device addition response: {response.status_code}")
            print(f"Device addition response content: {response.content.decode()}")
            self.assertEqual(response.status_code, 302)

        self.property_id = property.id  # Save property ID for subsequent tests
        print(f"Property ID for devices: {self.property_id}")

    def test_edit_device(self):
        print("Starting device editing test...")
        self.client.login(username=self.username, password=self.password)
        if not hasattr(self, 'property_id'):
            print("Property not found. Creating new property and devices...")
            self.test_add_devices()  # Ensure devices are added

        property = Property.objects.get(id=self.property_id)
        device = Device.objects.filter(property=property).first()  # Get the first created device for editing
        if not device:
            print("No device found. Adding a device...")
            self.test_add_devices()  # Ensure at least one device exists
            device = Device.objects.filter(property=property).first()

        response = self.client.post(reverse('edit_device', args=[property.id, device.id]), {
            'name': 'Updated Device Name',
            'key': device.key,
            'status': device.status,
        })
        print(f"Device edit response: {response.status_code}")
        print(f"Device edit response content: {response.content.decode()}")
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        print("Cleaning up the database...")
        # Optional: Clear data after tests
        User.objects.all().delete()
        Property.objects.all().delete()
        Device.objects.all().delete()
