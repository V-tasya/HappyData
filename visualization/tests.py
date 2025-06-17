import tempfile
import pandas as pd
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from uploading_and_processing_file.models import UploadedFile
from django.urls import reverse


class VisualizationTests(TestCase):
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

    def test_get_visualization_page(self):
        res = self.client.get(reverse('diagrams:graph'))
        self.assertEqual(res.status_code, 200)
        self.assertIn('graph_image_base64', res.context)

    def test_post_without_file(self):
        session = self.client.session
        session.pop('uploaded_file_id', None)
        session.save()

        res = self.client.post(reverse('diagrams:graph'), data={
            'generate_button': 'true',
            'select_plot': 'heatmap'
        })
        self.assertContains(res, "You need to upload file first.")

    def test_heatmap_success(self):
        res = self.client.post(reverse('diagrams:graph'), data={
            'generate_button': 'true',
            'select_plot': 'heatmap'
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn('graph_image_base64', res.context)
        self.assertIsNotNone(res.context['graph_image_base64'])

    def test_boxplot_success(self):
        res = self.client.post(reverse('diagrams:graph'), data={
            'generate_button': 'true',
            'select_plot': 'boxplot',
            'col1': 'name_product',
            'col2': 'price'
        })
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.context['graph_image_base64'])

    def test_invalid_column_error(self):
        res = self.client.post(reverse('diagrams:graph'), data={
            'generate_button': 'true',
            'select_plot': 'boxplot',
            'col1': 'wrong',
            'col2': 'price'
        })
        self.assertContains(res, "One or bouth columns do not exist")

    def test_violinplot_success(self):
        res = self.client.post(reverse('diagrams:graph'), data={
            'generate_button': 'true',
            'select_plot': 'violinplot',
            'col1': 'name_product',
            'col2': 'price'
        })
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.context['graph_image_base64'])

    def test_hystogram_success(self):
        res = self.client.post(reverse('diagrams:graph'), data={
            'generate_button': 'true',
            'select_plot': 'hystogram',
            'col1': 'price'
        })
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.context['graph_image_base64'])

def test_scatterplot_success(self):
        res = self.client.post(reverse('diagrams:graph'), data={
            'generate_button': 'true',
            'select_plot': 'scatterplot',
            'col1': 'name_product',
            'col2': 'price'
        })
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.context['graph_image_base64'])