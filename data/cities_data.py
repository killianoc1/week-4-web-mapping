# Sample cities data for API development
def _c(name, country, region, population, latitude, longitude,
       founded_year, is_capital, timezone, elevation_m):
    return {
        'name': name, 'country': country, 'region': region,
        'population': population, 'latitude': latitude, 'longitude': longitude,
        'founded_year': founded_year, 'is_capital': is_capital,
        'timezone': timezone, 'elevation_m': elevation_m,
    }

CITIES_DATA = [
    _c('Dublin', 'Ireland', 'Leinster', 1400000, 53.3498, -6.2603, 841, True, 'Europe/Dublin', 8),
    _c('London', 'United Kingdom', 'England', 9000000, 51.5074, -0.1278, 43, True, 'Europe/London', 11),
    _c('Paris', 'France', 'Île-de-France', 11000000, 48.8566, 2.3522, 259, True, 'Europe/Paris', 35),
    _c('Berlin', 'Germany', 'Brandenburg', 3700000, 52.5200, 13.4050, 1237, True, 'Europe/Berlin', 34),
    _c('Madrid', 'Spain', 'Community of Madrid', 6600000, 40.4168, -3.7038, 865, True, 'Europe/Madrid', 650),
    _c('Rome', 'Italy', 'Lazio', 2800000, 41.9028, 12.4964, -753, True, 'Europe/Rome', 21),
    _c('Amsterdam', 'Netherlands', 'North Holland', 900000, 52.3676, 4.9041, 1275, True, 'Europe/Amsterdam', -2),
    _c('Barcelona', 'Spain', 'Catalonia', 5500000, 41.3851, 2.1734, -15, False, 'Europe/Madrid', 12),
    _c('Munich', 'Germany', 'Bavaria', 1500000, 48.1351, 11.5820, 1158, False, 'Europe/Berlin', 520),
    _c('Vienna', 'Austria', 'Vienna', 1900000, 48.2082, 16.3738, -500, True, 'Europe/Vienna', 171),
    _c('Stockholm', 'Sweden', 'Stockholm County', 1600000, 59.3293, 18.0686, 1252, True, 'Europe/Stockholm', 28),
    _c('Copenhagen', 'Denmark', 'Capital Region', 800000, 55.6761, 12.5683, 1167, True, 'Europe/Copenhagen', 24),
    _c('Oslo', 'Norway', 'Østlandet', 700000, 59.9139, 10.7522, 1040, True, 'Europe/Oslo', 23),
    _c('Helsinki', 'Finland', 'Uusimaa', 650000, 60.1699, 24.9384, 1550, True, 'Europe/Helsinki', 26),
    _c('Warsaw', 'Poland', 'Masovian Voivodeship', 1800000, 52.2297, 21.0122, 1300, True, 'Europe/Warsaw', 100),
    _c('Prague', 'Czech Republic', 'Central Bohemia', 1300000, 50.0755, 14.4378, 885, True, 'Europe/Prague', 200),
    _c('Brussels', 'Belgium', 'Brussels-Capital', 1200000, 50.8503, 4.3517, 979, True, 'Europe/Brussels', 13),
    _c('Zurich', 'Switzerland', 'Zurich', 400000, 47.3769, 8.5417, -15, False, 'Europe/Zurich', 408),
    _c('Lisbon', 'Portugal', 'Lisbon', 2800000, 38.7223, -9.1393, -1200, True, 'Europe/Lisbon', 2),
    _c('Athens', 'Greece', 'Attica', 3200000, 37.9838, 23.7275, -3000, True, 'Europe/Athens', 70),
]