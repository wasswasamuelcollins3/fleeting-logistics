from django.test import TestCase
from django.urls import reverse


class PublicPagesTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fleeting Logistics')

    def test_about_page_renders(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About')

    def test_services_page_renders(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Services')

    def test_contact_page_renders(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact')

    def test_tracking_page_renders(self):
        response = self.client.get(reverse('tracking'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Track Your Shipment')
