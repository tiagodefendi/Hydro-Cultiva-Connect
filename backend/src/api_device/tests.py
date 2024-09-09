from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.models import Device, DeviceLog, Property
from django.utils import timezone
import json

class ApiDeviceTestCase(TestCase):
    def setUp(self):
        print("Setting up the test environment...")
        # Creating a test user
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'Passw0rd!2024'

        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
        print(f"Test user created: {self.username}")

        # Creating a test property and associating it with the user
        self.test_property = Property.objects.create(
            user=self.user,  # Associating the property with the test user
            name='Test Property',
            description='Test property',
            latitude=123.456,
            longitude=78.910
        )
        print("Test property created")

        # Creating test devices and associating them with the property
        self.sprinkler = Device.objects.create(
            property=self.test_property,
            type='Sprinkler',
            name='Test Sprinkler',
            key='T3ST3-T3ST3-T3ST3',
            status='Off'
        )
        self.tank = Device.objects.create(
            property=self.test_property,
            type='Tank',
            name='Test Tank',
            key='T3ST3-T3ST3-T3ST3',
            status='Off'
        )
        self.thermometer = Device.objects.create(
            property=self.test_property,
            type='Thermometer',
            name='Test Thermometer',
            key='T3ST3-T3ST3-T3ST3',
            status='Off'
        )
        self.hygrometer = Device.objects.create(
            property=self.test_property,
            type='Hygrometer',
            name='Test Hygrometer',
            key='T3ST3-T3ST3-T3ST3',
            status='Off'
        )
        self.camera = Device.objects.create(
            property=self.test_property,
            type='Camera',
            name='Test Camera',
            key='T3ST3-T3ST3-T3ST3',
            status='Off'
        )

        self.YOUTUBE_LIVE_LINKS = [
            'O0tTOcBrMTI',
            'Na0w3Mz46GA',
            'QKTNfEEeDnE',
            '4oStw0r33so',
            'tNkZsRW7h2c',
            '4xDzrJKXOOY',
            'QviXe8xvA50',
            'ROW9DiPsL98',
            'b_TW4NYsbOo',
            'yOuYY4AL_1U',
        ]
        print("Test devices created")

    def test_turn_on_device(self):
        print("Testing the turn_on_device view...")
        response = self.client.post(reverse('turn_on_device'), json.dumps({
            'id': self.sprinkler.id,
        }), content_type='application/json')
        print(f"Turn on response status: {response.status_code}")
        print(f"Turn on response content: {response.content.decode()}")
        self.assertEqual(response.status_code, 200)
        self.sprinkler.refresh_from_db()
        self.assertEqual(self.sprinkler.status, 'On')

    def test_turn_off_device(self):
        print("Testing the turn_off_device view...")
        # Ensuring the device is on first
        self.sprinkler.status = 'On'
        self.sprinkler.save()
        response = self.client.post(reverse('turn_off_device'), json.dumps({
            'id': self.sprinkler.id,
        }), content_type='application/json')
        print(f"Turn off response status: {response.status_code}")
        print(f"Turn off response content: {response.content.decode()}")
        self.assertEqual(response.status_code, 200)
        self.sprinkler.refresh_from_db()
        self.assertEqual(self.sprinkler.status, 'Off')

    def test_check_water(self):
        print("Testing the check_water view...")
        response = self.client.post(reverse('check_water'), json.dumps({
            'id': self.tank.id,
        }), content_type='application/json')
        print(f"Check water response status: {response.status_code}")
        print(f"Check water response content: {response.content.decode()}")
        self.assertEqual(response.status_code, 200)
        self.tank.refresh_from_db()
        self.assertRegex(self.tank.status, r'^\d+%$')  # Checks if it is in "<float>%" format

    def test_measure_temperature(self):
        print("Testing the measure_temperature view...")
        response = self.client.post(reverse('measure_temperature'), json.dumps({
            'id': self.thermometer.id,
        }), content_type='application/json')
        print(f"Measure temperature response status: {response.status_code}")
        print(f"Measure temperature response content: {response.content.decode()}")
        self.assertEqual(response.status_code, 200)
        self.thermometer.refresh_from_db()
        self.assertRegex(self.thermometer.status, r'^\d+°C$')  # Checks if it is in "<float>°C" format

    def test_measure_humidity(self):
        print("Testing the measure_humidity view...")
        response = self.client.post(reverse('measure_humidity'), json.dumps({
            'id': self.hygrometer.id,
        }), content_type='application/json')
        print(f"Measure humidity response status: {response.status_code}")
        print(f"Measure humidity response content: {response.content.decode()}")
        self.assertEqual(response.status_code, 200)
        self.hygrometer.refresh_from_db()
        self.assertRegex(self.hygrometer.status, r'^\d+%$')  # Checks if it is in "<float>%" format

    def test_device_live(self):
        print("Testing the live view...")
        # Assuming self.camera is a 'Camera' type device
        response = self.client.post(reverse('live'), 
                                    json.dumps({'id': self.camera.id}),
                                    content_type='application/json')
        print(f"Live response status: {response.status_code}")
        print(f"Live response content: {response.content.decode()}")

        # Check the response status
        self.assertEqual(response.status_code, 200)
        
        # Check the response content
        response_data = json.loads(response.content)
        self.assertIn('live', response_data)
        self.assertIn(response_data['live'], self.YOUTUBE_LIVE_LINKS)

        # Check if the device status was updated
        self.camera.refresh_from_db()
        self.assertEqual(self.camera.status, 'Live')

    def tearDown(self):
        # Cleaning up the data created after tests
        Device.objects.all().delete()
        Property.objects.all().delete()
        User.objects.all().delete()
        print("Test data cleaned up after test execution")
