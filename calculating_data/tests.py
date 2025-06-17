import tempfile
import pandas as pd
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from uploading_and_processing_file.models import UploadedFile
from django.urls import reverse


class CalculatingViewsTests(TestCase):
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

    def test_basic_data_view(self):
        res = self.client.post(reverse('calculate:calculate_info'))
        self.assertEqual(res.status_code, 200)
        json = res.json()
        self.assertEqual(json['number_of_col'], 3)
        self.assertEqual(json['number_of_rows'], 3)
        self.assertEqual(json['number_of_num_val'], 2)
        self.assertEqual(json['mess1'], 'Filled')

    def test_get_numeric_columns(self):
        res = self.client.post(reverse('calculate:get_num_cols'))
        self.assertEqual(res.status_code, 200)
        json = res.json()
        self.assertIn('number_of_products', json['numeric_columns'])
        self.assertIn('price', json['numeric_columns'])
        self.assertNotIn('name_of_product', json['numeric_columns'])

    def test_calculate_data_valid_column(self):
        res = self.client.post(
            reverse('calculate:calculate_data'),
            content_type='application/json',
            data={'column': 'price'}
        )
        self.assertEqual(res.status_code, 200)
        json = res.json()
        self.assertEqual(json['mess2'], 'Calculated')
        self.assertAlmostEqual(json['mean_val'], 80.17, places=1)
        self.assertEqual(json['median_val'], 80.0)

    def test_calculate_data_invalid_column(self):
        res = self.client.post(
            reverse('calculate:calculate_data'),
            content_type='application/json',
            data={'column': 'not_exist'}
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('error', res.json())