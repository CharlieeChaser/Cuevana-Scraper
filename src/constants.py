import os

# Prefijos de IDs
ID_PREFIX = 'cuevanap_'
IMDB_PREFIX = 'tt'

# URLs de Cuevana.pro
CUEVANA_PRO_URL = 'https://cuevana.pro/'
CUEVANA_PRO_API = 'https://api.cuevana.pro/'

# Configuración del servidor
PORT = int(os.getenv('PORT', 55323))
HOST = os.getenv('HOST', '0.0.0.0')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# APIs externas
TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')
OMDB_API_KEY = os.getenv('OMDB_API_KEY', '')

# Configuración del addon
ADDON_ID = 'me.charliechaser.cuevana-pro'
ADDON_NAME = 'Cuevana Pro'
ADDON_VERSION = '1.0.0'
ADDON_DESCRIPTION = 'Browse and watch movies and series from Cuevana.pro'
ADDON_LOGO = 'https://cuevana.pro/assets/logo.png'

# Thresholds
IMDB_SIMILARITY_THRESHOLD = 0.6
SEARCH_LIMIT = 20