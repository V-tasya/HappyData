from django.test import TestCase
from django.urls import reverse

class InterfaceViewsTest(TestCase):

    def test_main_page_status_code(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

    def test_main_page_template_used(self):
        res = self.client.get('/')
        self.assertTemplateUsed(res, 'main_page.html')

    def test_analysis_page_status_code(self):
        res = self.client.get('/analysis/')
        self.assertEqual(res.status_code, 200)

    def test_analysis_page_template_used(self):
        res = self.client.get('/analysis/')
        self.assertTemplateUsed(res, 'analysis_page.html')