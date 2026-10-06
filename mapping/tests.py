from django.contrib.staticfiles import finders
from django.test import TestCase


class MapViewTests(TestCase):
    def test_map_view_loads(self):
        """The map page loads and pulls in Leaflet."""
        for url in ('/', '/map/'):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Leaflet', response.content.decode())
            self.assertIn('id="map"', response.content.decode())

    def test_static_files_found(self):
        """Static assets exist where STATICFILES_DIRS expects them.

        The test client runs with DEBUG=False, so Django does not serve
        /static/ here; check the finders instead of requesting the URL.
        """
        self.assertIsNotNone(finders.find('js/map.js'))
        self.assertIsNotNone(finders.find('css/styles.css'))
