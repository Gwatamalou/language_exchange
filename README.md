# Language Exchange

Language Exchange is a platform for learning languages through live communication via online video and text chat.

## Features

- **Online video and text chat** for language learning.
- Real-time communication powered by Django Channels and Redis.

## Requirements

- Python 3.10
- Django 5.0
- Redis (for real-time communication)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Gwatamalou/language_exchange.git
   cd language_exchange
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Set up a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate   # On Windows
   ```

4. (Optional) Install Daphne support for Django Channels:

   ```bash
   python3 -m pip install -U 'channels[daphne]'  # On Linux/Mac
   python -m pip install -U "channels[daphne]"  # On Windows
   ```

## Configuration

### Local Setup

For local development, ensure Redis is running locally on port `6379`, and configure the `CHANNEL_LAYERS` in `settings.py`:

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}
```

### Docker Setup

For deployment with Docker, use the provided `docker-compose.yml` file in the project root. Configure the `CHANNEL_LAYERS` in `settings.py` as follows:

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(os.getenv("REDIS_HOST", "redis"), 6379)],
        },
    },
}
```

## Running the Project

### Locally

To run the project locally, use the standard Django development server:

```bash
python manage.py runserver
```

### With Docker

To run the project with Docker:

```bash
docker-compose up
```

## Testing

Unit tests are available for forms and models in the `users` app. Run the tests with:

```bash
python manage.py test users.tests
```

## Database

- Default: SQLite
- Redis is used for managing WebSocket communication.

