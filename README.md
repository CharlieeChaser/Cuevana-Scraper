# Cuevana Scraper

A powerful and efficient web scraper for extracting movie and TV show information from Cuevana streaming platform. This project provides a robust solution for collecting, parsing, and managing content metadata with built-in support for filtering, pagination, and data export.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Features

- 🎬 **Comprehensive Content Scraping**: Extract movie and TV show information including titles, descriptions, ratings, and metadata
- 🔄 **Robust Error Handling**: Built-in retry mechanisms and error recovery
- 🔍 **Advanced Filtering**: Filter content by genre, year, rating, and other criteria
- 📊 **Data Export**: Support for multiple export formats (JSON, CSV, Excel)
- ⚡ **High Performance**: Optimized parsing and concurrent requests
- 🛡️ **Respectful Scraping**: Implements rate limiting and respects robots.txt
- 🗄️ **Database Support**: Optional integration with various databases
- 🔐 **Secure**: Handles sensitive data with proper encryption
- 📝 **Comprehensive Logging**: Detailed logs for debugging and monitoring
- 🧪 **Well-tested**: Includes unit and integration tests

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- git
- Virtual environment support (recommended)

### Step-by-Step Installation

1. **Clone the repository**:
```bash
git clone https://github.com/CharlieeChaser/Cuevana-Scraper.git
cd Cuevana-Scraper
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Install optional dependencies** (for specific features):
```bash
# For database support
pip install -r requirements-db.txt

# For development and testing
pip install -r requirements-dev.txt

# All extras
pip install -e ".[all]"
```

5. **Verify installation**:
```bash
python -c "import cuevana_scraper; print(cuevana_scraper.__version__)"
```

## Configuration

### Configuration File

Create a `.env` file in the project root directory:

```env
# Scraper Settings
SCRAPER_MODE=production
LOG_LEVEL=INFO
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36

# Rate Limiting
REQUEST_TIMEOUT=10
RETRY_ATTEMPTS=3
RETRY_DELAY=2
REQUEST_DELAY=1

# Database Configuration (Optional)
DATABASE_TYPE=sqlite  # sqlite, postgresql, mysql, mongodb
DATABASE_URL=sqlite:///cuevana_data.db
# For PostgreSQL: postgresql://user:password@localhost:5432/cuevana_db

# Output Settings
OUTPUT_FORMAT=json  # json, csv, excel
OUTPUT_DIR=./output

# Proxy Settings (Optional)
USE_PROXY=false
PROXY_URL=http://proxy.example.com:8080
PROXY_USERNAME=
PROXY_PASSWORD=

# API Settings
ENABLE_API_MODE=false
API_PORT=5000
API_HOST=127.0.0.1

# Feature Flags
ENABLE_CACHING=true
ENABLE_COMPRESSION=false
VERIFY_SSL=true
```

### Configuration Options Explained

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `SCRAPER_MODE` | string | `production` | Operating mode (development, testing, production) |
| `LOG_LEVEL` | string | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `USER_AGENT` | string | - | Custom User-Agent header for requests |
| `REQUEST_TIMEOUT` | int | 10 | Request timeout in seconds |
| `RETRY_ATTEMPTS` | int | 3 | Number of retry attempts for failed requests |
| `RETRY_DELAY` | int | 2 | Delay between retries in seconds |
| `REQUEST_DELAY` | int | 1 | Delay between requests in seconds |
| `DATABASE_TYPE` | string | `sqlite` | Database engine to use |
| `DATABASE_URL` | string | - | Database connection string |
| `OUTPUT_FORMAT` | string | `json` | Default output format |
| `OUTPUT_DIR` | string | `./output` | Directory for output files |

## Usage

### Basic Usage

#### 1. Scrape All Movies

```python
from cuevana_scraper import CuevanaScraper

scraper = CuevanaScraper()
movies = scraper.scrape_movies()
scraper.export_data(movies, format='json', filename='movies.json')
```

#### 2. Scrape with Filters

```python
from cuevana_scraper import CuevanaScraper, Filters

scraper = CuevanaScraper()

# Create filters
filters = Filters(
    genre='Action',
    year_from=2020,
    year_to=2024,
    min_rating=7.0
)

# Scrape with filters
movies = scraper.scrape_movies(filters=filters)
```

#### 3. Scrape TV Shows

```python
from cuevana_scraper import CuevanaScraper

scraper = CuevanaScraper()
tv_shows = scraper.scrape_tv_shows()
scraper.export_data(tv_shows, format='csv', filename='tv_shows.csv')
```

#### 4. Scrape Specific Content

```python
from cuevana_scraper import CuevanaScraper

scraper = CuevanaScraper()

# Scrape by URL
content = scraper.scrape_url('https://www.cuevana.tv/pelicula/12345')

# Scrape by search term
results = scraper.search('Inception')
```

#### 5. Handle Pagination

```python
from cuevana_scraper import CuevanaScraper

scraper = CuevanaScraper()

# Scrape with pagination
for page in range(1, 6):
    movies = scraper.scrape_movies(page=page, items_per_page=20)
    scraper.export_data(movies, format='json', filename=f'movies_page_{page}.json')
```

### Command Line Usage

```bash
# Display help
python -m cuevana_scraper --help

# Scrape movies
python -m cuevana_scraper scrape movies --output movies.json

# Scrape TV shows with filters
python -m cuevana_scraper scrape tv-shows \
  --genre "Action" \
  --min-rating 7.0 \
  --output tv_shows.json

# Search for specific content
python -m cuevana_scraper search "The Matrix" --output results.json

# Export database to CSV
python -m cuevana_scraper export --format csv --output data.csv

# Update existing data
python -m cuevana_scraper update --mode incremental
```

### Advanced Usage

#### Custom Session Configuration

```python
from cuevana_scraper import CuevanaScraper
import requests

scraper = CuevanaScraper()

# Create custom session
session = requests.Session()
session.headers.update({
    'User-Agent': 'Custom-Agent/1.0',
    'Accept-Language': 'en-US'
})

scraper.set_session(session)
movies = scraper.scrape_movies()
```

#### Database Integration

```python
from cuevana_scraper import CuevanaScraper, DatabaseManager

scraper = CuevanaScraper()
db_manager = DatabaseManager(db_url='postgresql://user:pass@localhost/cuevana_db')

# Scrape and store in database
movies = scraper.scrape_movies()
db_manager.save_movies(movies)

# Query from database
action_movies = db_manager.query_movies(genre='Action', min_rating=7.0)
```

#### Error Handling

```python
from cuevana_scraper import CuevanaScraper, ScraperException

scraper = CuevanaScraper()

try:
    movies = scraper.scrape_movies()
except ScraperException as e:
    print(f"Scraping error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Deployment

### Docker Deployment

1. **Build Docker image**:
```bash
docker build -t cuevana-scraper:latest .
```

2. **Run with Docker**:
```bash
docker run -d \
  --name cuevana-scraper \
  -e LOG_LEVEL=INFO \
  -e DATABASE_URL=postgresql://user:pass@db:5432/cuevana \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/.env:/app/.env \
  cuevana-scraper:latest
```

3. **Docker Compose** (recommended for production):
```bash
docker-compose up -d
```

### Kubernetes Deployment

1. **Build and push image**:
```bash
docker tag cuevana-scraper:latest your-registry/cuevana-scraper:latest
docker push your-registry/cuevana-scraper:latest
```

2. **Deploy using kubectl**:
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/configmap.yaml
```

3. **Monitor deployment**:
```bash
kubectl get pods -l app=cuevana-scraper
kubectl logs -f deployment/cuevana-scraper
```

### Manual Deployment

1. **Server Setup**:
```bash
# SSH into your server
ssh user@your-server.com

# Clone repository
git clone https://github.com/CharlieeChaser/Cuevana-Scraper.git
cd Cuevana-Scraper

# Setup Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure systemd Service** (Linux):
Create `/etc/systemd/system/cuevana-scraper.service`:
```ini
[Unit]
Description=Cuevana Scraper Service
After=network.target

[Service]
Type=simple
User=cuevana
WorkingDirectory=/opt/Cuevana-Scraper
Environment="PATH=/opt/Cuevana-Scraper/venv/bin"
ExecStart=/opt/Cuevana-Scraper/venv/bin/python -m cuevana_scraper run
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. **Enable and start service**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable cuevana-scraper
sudo systemctl start cuevana-scraper
```

### Environment Variables for Production

```env
# Security
SECRET_KEY=your-secret-key-here
API_KEY=your-api-key-here

# Database
DATABASE_URL=postgresql://user:secure_password@db.example.com:5432/cuevana_prod

# Logging
LOG_LEVEL=WARNING
LOG_FILE=/var/log/cuevana-scraper/app.log

# Performance
WORKER_PROCESSES=4
MAX_CONNECTIONS=20

# Monitoring
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
ENABLE_METRICS=true
METRICS_PORT=9090
```

## Contributing

We welcome contributions from the community! Please follow these guidelines to ensure a smooth collaboration.

### Code of Conduct

- Be respectful and inclusive
- Maintain professional communication
- Report issues constructively
- Help others in the community

### Getting Started with Development

1. **Fork the repository**:
Click the "Fork" button on GitHub to create your own copy.

2. **Clone your fork**:
```bash
git clone https://github.com/YOUR-USERNAME/Cuevana-Scraper.git
cd Cuevana-Scraper
```

3. **Create a development branch**:
```bash
git checkout -b feature/your-feature-name
```

4. **Install development dependencies**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

### Development Workflow

1. **Make your changes**:
   - Write clean, readable code
   - Follow PEP 8 style guide
   - Add comments for complex logic
   - Update documentation as needed

2. **Write or update tests**:
```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=cuevana_scraper tests/

# Run specific test file
pytest tests/test_scraper.py -v
```

3. **Code quality checks**:
```bash
# Format code
black cuevana_scraper/

# Check style
flake8 cuevana_scraper/

# Type checking
mypy cuevana_scraper/

# Security check
bandit -r cuevana_scraper/
```

4. **Run full test suite**:
```bash
./scripts/run_tests.sh
```

### Commit Guidelines

- Use clear, descriptive commit messages
- Reference related issues when applicable
- Keep commits focused and atomic

Examples:
```bash
git commit -m "Add movie filtering by genre and year"
git commit -m "Fix: Handle timeout errors gracefully (fixes #123)"
git commit -m "docs: Update README with new API endpoints"
```

### Pull Request Process

1. **Push your branch**:
```bash
git push origin feature/your-feature-name
```

2. **Create a Pull Request**:
   - Go to GitHub and click "Compare & pull request"
   - Provide a clear title and description
   - Reference any related issues (#123)
   - Include a checklist of changes

3. **PR Description Template**:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #123

## Changes Made
- Change 1
- Change 2

## Testing
Describe testing performed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
```

4. **Review Process**:
   - Maintainers will review your PR
   - Address feedback and make requested changes
   - Once approved, your PR will be merged

### Reporting Issues

1. **Check existing issues** to avoid duplicates
2. **Use issue templates** provided
3. **Include detailed information**:
   - Python version and OS
   - Exact error messages
   - Steps to reproduce
   - Expected vs actual behavior

### Style Guidelines

```python
# Good
def scrape_movies(self, filters=None, page=1):
    """
    Scrape movies from Cuevana.
    
    Args:
        filters (Filters, optional): Filtering criteria
        page (int, optional): Page number. Defaults to 1.
    
    Returns:
        list: List of movie dictionaries
    """
    pass

# Bad
def scrape_movies(filters, page):
    # scrape movies
    return movies
```

### Documentation Standards

- Use clear, concise language
- Include code examples
- Document parameters and return values
- Update docstrings with changes
- Keep README.md current

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

### Getting Help

- 📖 **Documentation**: Check the [docs](docs/) folder
- 💬 **Discussions**: Use GitHub Discussions for questions
- 🐛 **Issues**: Report bugs on GitHub Issues
- 📧 **Email**: contact@example.com

### Additional Resources

- [Cuevana Website](https://www.cuevana.tv)
- [Python Requests Documentation](https://docs.python-requests.org/)
- [BeautifulSoup4 Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Acknowledgments

- Thanks to all contributors
- Community feedback and suggestions
- Open-source libraries used in this project

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes in each version.

---

**Last Updated**: January 3, 2026  
**Current Version**: 1.0.0  
**Status**: Active Development

For the latest information, visit the [GitHub repository](https://github.com/CharlieeChaser/Cuevana-Scraper).
