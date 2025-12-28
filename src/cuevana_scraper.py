import requests
from bs4 import BeautifulSoup
import cloudscraper
import logging
from typing import List, Dict, Optional
from urllib.parse import urljoin, quote
from .constants import CUEVANA_PRO_URL, ID_PREFIX

logger = logging.getLogger(__name__)

class CuevanaScraper:
    def __init__(self):
        """Inicializa el scraper de Cuevana.pro"""
        self.base_url = CUEVANA_PRO_URL
        self.session = cloudscraper.create_scraper()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_movies(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Busca películas en Cuevana.pro
        
        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados
            
        Returns:
            Lista de películas encontradas
        """
        try:
            search_url = f"{self.base_url}?s={quote(query)}"
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            movies = []
            
            # Ajusta estos selectores según la estructura actual de Cuevana.pro
            for item in soup.select('.movie-item, .film-item, article')[:limit]:
                try: 
                    movie = self._parse_movie_item(item)
                    if movie:
                        movies.append(movie)
                except Exception as e:
                    logger.warning(f"Error parsing movie item: {e}")
                    continue
            
            return movies
        except Exception as e:
            logger.error(f"Error searching movies: {e}")
            return []
    
    def get_top_movies(self, limit: int = 30) -> List[Dict]:
        """
        Obtiene las películas más vistas/destacadas
        
        Args:
            limit: Número máximo de resultados
            
        Returns:
            Lista de películas destacadas
        """
        try: 
            response = self.session.get(f"{self.base_url}peliculas/", timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            movies = []
            
            for item in soup.select('.movie-item, .film-item')[:limit]:
                try: 
                    movie = self._parse_movie_item(item)
                    if movie:
                        movies.append(movie)
                except Exception as e:
                    logger.warning(f"Error parsing movie item: {e}")
                    continue
            
            return movies
        except Exception as e:
            logger.error(f"Error getting top movies: {e}")
            return []
    
    def get_series(self, query: str = None, limit: int = 20) -> List[Dict]:
        """
        Obtiene series de TV
        
        Args:
            query: Término de búsqueda (opcional)
            limit: Número máximo de resultados
            
        Returns:
            Lista de series
        """
        try: 
            if query:
                url = f"{self.base_url}?s={quote(query)}&type=tv"
            else:
                url = f"{self.base_url}series/"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            series = []
            
            for item in soup.select('.series-item, .tv-item')[:limit]:
                try:
                    show = self._parse_series_item(item)
                    if show:
                        series.append(show)
                except Exception as e:
                    logger.warning(f"Error parsing series item: {e}")
                    continue
            
            return series
        except Exception as e:
            logger.error(f"Error getting series: {e}")
            return []
    
    def get_movie_details(self, movie_url: str) -> Optional[Dict]:
        """
        Obtiene los detalles completos de una película
        
        Args:
            movie_url: URL de la película
            
        Returns:
            Diccionario con detalles de la película
        """
        try:
            response = self.session.get(movie_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            details = {
                'url': movie_url,
                'title': self._extract_title(soup),
                'description': self._extract_description(soup),
                'poster': self._extract_poster(soup),
                'year': self._extract_year(soup),
                'rating': self._extract_rating(soup),
                'runtime': self._extract_runtime(soup),
                'genres': self._extract_genres(soup),
            }
            
            return details
        except Exception as e:
            logger.error(f"Error getting movie details: {e}")
            return None
    
    def get_streams(self, movie_url: str) -> List[Dict]:
        """
        Obtiene los enlaces de reproducción disponibles
        
        Args: 
            movie_url: URL de la película
            
        Returns: 
            Lista de streams disponibles
        """
        try:
            response = self.session.get(movie_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            streams = []
            
            # Busca los servidores de video disponibles
            # Ajusta los selectores según Cuevana.pro
            for stream_elem in soup.select('.server-item, .stream-link, .player-link'):
                try: 
                    stream = self._parse_stream(stream_elem)
                    if stream:
                        streams.append(stream)
                except Exception as e:
                    logger.warning(f"Error parsing stream: {e}")
                    continue
            
            return streams
        except Exception as e:
            logger.error(f"Error getting streams: {e}")
            return []
    
    # Métodos auxiliares para parsing
    
    def _parse_movie_item(self, element) -> Optional[Dict]:
        """Parsea un elemento de película de la lista"""
        try:
            # Ajusta los selectores según la estructura de Cuevana.pro
            title = element.select_one('h2, .title, .name')
            link = element.select_one('a')
            poster = element.select_one('img')
            year = element.select_one('.year, .date')
            
            if not title or not link: 
                return None
            
            movie_url = link.get('href', '')
            if not movie_url.startswith('http'):
                movie_url = urljoin(self.base_url, movie_url)
            
            return {
                'type': 'movie',
                'id': ID_PREFIX + movie_url,
                'name': title.get_text(strip=True),
                'poster': poster.get('src', poster.get('data-src')) if poster else '',
                'year': year.get_text(strip=True) if year else '',
                'url': movie_url
            }
        except Exception as e:
            logger.warning(f"Error parsing movie item: {e}")
            return None
    
    def _parse_series_item(self, element) -> Optional[Dict]:
        """Parsea un elemento de serie de la lista"""
        try:
            title = element.select_one('h2, .title, .name')
            link = element.select_one('a')
            poster = element.select_one('img')
            year = element.select_one('.year, .date')
            
            if not title or not link:
                return None
            
            series_url = link.get('href', '')
            if not series_url.startswith('http'):
                series_url = urljoin(self.base_url, series_url)
            
            return {
                'type': 'series',
                'id': ID_PREFIX + series_url,
                'name': title.get_text(strip=True),
                'poster': poster.get('src', poster.get('data-src')) if poster else '',
                'year': year.get_text(strip=True) if year else '',
                'url': series_url
            }
        except Exception as e:
            logger.warning(f"Error parsing series item: {e}")
            return None
    
    def _parse_stream(self, element) -> Optional[Dict]:
        """Parsea un elemento de stream"""
        try:
            server_name = element.get_text(strip=True)
            stream_url = element.get('href', element.get('data-url'))
            
            if not stream_url:
                return None
            
            return {
                'url': stream_url,
                'title': f"📺 {server_name}",
                'server': server_name
            }
        except Exception as e:
            logger.warning(f"Error parsing stream: {e}")
            return None
    
    def _extract_title(self, soup) -> str:
        """Extrae el título de la página"""
        title = soup.select_one('h1, .title, .movie-title')
        return title.get_text(strip=True) if title else ''
    
    def _extract_description(self, soup) -> str:
        """Extrae la descripción/sinopsis"""
        desc = soup.select_one('.description, .synopsis, .plot, p')
        return desc.get_text(strip=True) if desc else ''
    
    def _extract_poster(self, soup) -> str:
        """Extrae la URL del póster"""
        poster = soup.select_one('img.poster, img.thumbnail')
        if poster:
            return poster.get('src') or poster.get('data-src') or ''
        return ''
    
    def _extract_year(self, soup) -> str:
        """Extrae el año de lanzamiento"""
        year = soup.select_one('.year, .release-year')
        return year.get_text(strip=True) if year else ''
    
    def _extract_rating(self, soup) -> str:
        """Extrae la calificación"""
        rating = soup.select_one('.rating, .score, [data-rating]')
        return rating.get_text(strip=True) if rating else ''
    
    def _extract_runtime(self, soup) -> str:
        """Extrae la duración"""
        runtime = soup.select_one('.runtime, .duration')
        return runtime.get_text(strip=True) if runtime else ''
    
    def _extract_genres(self, soup) -> List[str]:
        """Extrae los géneros"""
        genres = []
        for genre in soup.select('.genre, .tag, [data-genre]'):
            genre_text = genre.get_text(strip=True)
            if genre_text:
                genres.append(genre_text)
        return genres
