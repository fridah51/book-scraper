A fastAPI system for crawling, detecting changes, and serving book data from https://books.toscrape.com.
# BooksToScrape Crawler & API System

## Features

✔ Async crawler using httpx & asyncio  
✔ MongoDB storage with deduplication  
✔ Daily scheduler with change detection  
✔ Change logs and daily report  
✔ Secure FastAPI REST API with API key  
✔ Filtering, sorting, pagination  
✔ Pydantic validation  
✔ Retry logic and fault handling  
✔ Dockerized MongoDB  
✔ Resume crawl support  
✔ Content hashing for change detection  

---

## Architecture
Fk assgn/
│
├── api/ # REST API
├── crawler/ # Async crawler logic
├── scheduler/ # APScheduler jobs
├── db/ # MongoDB connection
├── models/ # Pydantic schemas
├── scripts/ # Manual triggers
├── utils/ # Logging & helpers
├── tests/ # Unit tests
│
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md

# Setup Instructions

```bash
    1. Clone Repository
        git clone https://github.com/fridah51/book-scraper

    2.Create Virtual Environment
        python -m venv venv
        venv\Scripts\activate

    3. Install dependencies
        pip install -r requirements.txt

    4. Environment Variables
        Create .env file

        # Sample .env file 
        MONGO_URI=mongodb://mongo:27017
        DATABASE_NAME=booksdb
        API_KEYS=key1,key2
        REDIS_URL=redis://redis:6379/0

        RATE_LIMIT=100/hour
        CRAWL_CONCURRENCY=10
        LOG_LEVEL=INFO

    5. Spin Up MongoDB (Docker)
        docker run -d -p -27017:27017 mongo

    6. Start API Server
        uvicorn main:app --reload

        Visit Swagger UI :
        http://localhost:8000/docs
        
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
            pytest