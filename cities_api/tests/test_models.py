from django.test import TestCase
from django.contrib.gis.geos import Point
from cities_api.models import City


class CityModelTests(TestCase):

    def test_population_category(self):
        c = City(name='X', country='Y', population=6_000_000,
                 location=Point(0, 0, srid=4326))
        self.assertEqual(c.population_category, "Large Metropolis")

    def test_coordinates_are_lon_lat(self):
        c = City(name='X', country='Y', population=1,
                 location=Point(-6.26, 53.35, srid=4326))
        self.assertEqual(c.coordinates, [-6.26, 53.35])
        self.assertEqual(c.latitude, 53.35)
        self.assertEqual(c.longitude, -6.26)

    def test_str(self):
        c = City(name='Dublin', country='Ireland', population=1,
                 location=Point(0, 0, srid=4326))
        self.assertEqual(str(c), "Dublin, Ireland")

    def test_bounding_box_manager(self):
        City.objects.create(name='In', country='Y', population=1,
                            location=Point(1, 1, srid=4326))
        City.objects.create(name='Out', country='Y', population=1,
                            location=Point(50, 50, srid=4326))
        self.assertEqual(City.objects.in_bounding_box([0, 0, 2, 2]).count(), 1)

    def test_within_radius_manager(self):
        dublin = City.objects.create(name='Dublin', country='Ireland', population=1,
                                     location=Point(-6.2603, 53.3498, srid=4326))
        City.objects.create(name='Paris', country='France', population=1,
                            location=Point(2.3522, 48.8566, srid=4326))
        nearby = City.objects.within_radius(dublin.location, 100)
        self.assertEqual([c.name for c in nearby], ['Dublin'])