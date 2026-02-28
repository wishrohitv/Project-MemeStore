### Setup guide


# Setup .env file

Create a `.env` file in the backend/.env of your project and add the following environment variables:

```bash
APP_SECRET_KEY="your_secret_key" # A random string used for signing tokens and other secrets

ORIGINS="http://127.0.0.1:8000" # Comma-separated list of allowed origins for CORS. For development, you can set it to http://

DB_URL="postgresql://username:password@localhost:5432/memestore"

CLOUDINARY_URL="cloudinary://api_key:api_secret@cloud_name" # Optional, only needed if you want to use Cloudinary for image storage

RESEND_API_KEY="your_resend_api_key" # Optional, only needed if you want to use Resend for email sending

REDIS_URL="redis://localhost:6379" # Optional, only needed if you want to use Redis for caching

```