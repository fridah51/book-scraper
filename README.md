# Books To Scrape Crawler & API System

A FastAPI system for crawling, detecting changes, and serving book data from https://books.toscrape.com.


## Architecture
book-scraper/
│
├── api/ # REST API
├── crawler/ # Async crawler logic
├── scheduler/ # APScheduler jobs
├── db/ # MongoDB connection
├── models/ # Pydantic schemas
├── scripts/ # Manual triggers
├── utilitiess/ # Logging & helpers
├── tests/ # Unit tests
│
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md

## Setup Instructions

```bash
    1. Clone Repository
        git clone https://github.com/fridah51/book-scraper

    2.Create Virtual Environment
        python -m venv venv
        venv\Scripts\activate

    3. Install dependencies
        python 3.13
        pip install -r requirements.txt

    4. Environment Variables
        Create .env file

        # Sample .env file 
        MONGO_URI=mongodb://mongo:27017
        DATABASE_NAME=booksdb
        API_KEYS=key1,key2


    5. Spin Up MongoDB using Docker image mongo
        docker run -d -p -27017:27017 mongo

    6. Start API Server
        locally: uvicorn main:app --reload
            Visit Swagger UI : http://localhost:8000/docs
            docker : docker compose up -d 
        
    7. API Endpoints
    GET /books

        Filters:
            category
            min_price
            max_price
            rating

        Supports:

        sort_by = rating | price | reviews

        page / per_page

    GET /books/{id}
        Returns full book details

    GET /changes
        Shows history of updates

    8. Authentication
        Include header:
            X-API-Key: supersecretkey123

    9. Reports
        Scheduler generates:

            /reports/change_report_YYYY-MM-DD.json

    10. Testing
        Run:
            pytest -v








INFO:     Waiting for application startup.
[2025-11-30 17:22:46] [INFO] [scheduler.jobs] Scheduler started. Waiting for jobs...
INFO:     Application startup complete.
[2025-11-30 17:24:00] [INFO] [scheduler.jobs] Starting scheduled daily crawl...
No more pages after page 50
[2025-11-30 17:39:02] [INFO] [scheduler.jobs] Scheduled Crawl finished successfully
Report generated for 2025-11-30
[2025-11-30 17:39:02] [INFO] [scheduler.jobs] Daily change report generated