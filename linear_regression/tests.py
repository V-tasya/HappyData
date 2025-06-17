from django.test import TestCase, Client
import tempfile
import pandas as pd
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from uploading_and_processing_file.models import UploadedFile


class LinearRegressionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.df = pd.DataFrame({
            'number_of_products': [10, 20, 30],
            'name_product': ['pot', 'pensil', 'case'],
            'price': [70.0, 80.0, 90.5]
        })

        self.temp_csv = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
        self.df.to_csv(self.temp_csv.name, index=False)

        with open(self.temp_csv.name, 'rb') as f:
            uploaded = UploadedFile.objects.create(
                file=SimpleUploadedFile('test.csv', f.read(), content_type='text/csv')
            )

        self.file_id = uploaded.id
        session = self.client.session
        session['uploaded_file_id'] = self.file_id
        session.save()

    def test_get_regression_page(self):
        res = self.client.get(reverse('regression:line-reg'))
        self.assertEqual(res.status_code, 200)

    def test_post_no_target_column(self):
        res = self.client.post(reverse('regression:line-reg'), {
            'predict_button': 'true',
            'target_column': ''
        })
        self.assertContains(res, 'Please enter target column name.')

    def test_post_invalid_target_column(self):
        res = self.client.post(reverse('regression:line-reg'), {
            'predict_button': 'true',
            'target_column': 'not_existing_column'
        })
        self.assertContains(res, 'Target column was not found')

    def test_post_non_numeric_target_column(self):
        res = self.client.post(reverse('regression:line-reg'), {
            'predict_button': 'true',
            'target_column': 'name_product'
        })
        self.assertContains(res, 'Target column should contain numerical values')

    def test_successful_regression(self):
        res = self.client.post(reverse('regression:line-reg'), {
            'predict_button': 'true',
            'target_column': 'price'
        })

        self.assertEqual(res.status_code, 200)
        self.assertIn('mae', res.context)
        self.assertIn('rmse', res.context)
        self.assertIn('regression_graph_base64', res.context)
        self.assertIsNotNone(res.context['regression_graph_base64'])