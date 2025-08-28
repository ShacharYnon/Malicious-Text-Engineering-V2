# Malicious-Text-Engineering-V2

A Kafka-based system for processing and analyzing malicious text content, specifically focused on antisemitic content detection and analysis.

## System Architecture

The system consists of 5 microservices:

1. **Data Retrieval Service**: FastAPI service for retrieving processed data
2. **Retriever Service**: Fetches data from MongoDB and publishes to Kafka
3. **Preprocessor Service**: Cleans and preprocesses text data
4. **Enricher Service**: Adds sentiment analysis and weapons detection
5. **Persister Service**: Stores enriched data back to MongoDB

## Services

### Data Retrieval (`services/data-retrival`)
- **Port**: 8000
- **Endpoints**: 
  - `/health` - Health check
  - `/tweets/antisemitic` - Get antisemitic tweets
  - `/tweets/not-antisemitic` - Get non-antisemitic tweets

### Retriever (`services/retriver`)
- Fetches oldest documents from MongoDB
- Publishes to Kafka topics based on antisemitic classification

### Preprocessor (`services/preprocessor`)
- Consumes raw tweets from Kafka
- Cleans text using NLTK and stopword removal
- Publishes processed tweets

### Enricher (`services/enricher`)
- Adds sentiment analysis using NLTK VADER
- Detects weapons mentions in text
- Publishes enriched documents

### Persister (`services/presister`)
- Consumes enriched documents
- Stores final results in MongoDB collections

## Setup and Running

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Stop services
docker-compose down
```

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start individual services:
```bash
# Data Retrieval API
python -m services.data-retrival.src.main

# Retriever
python -m services.retriver.src.main

# Preprocessor
python -m services.preprocessor.src.main

# Enricher
python -m services.enricher.src.main

# Persister
python -m services.presister.src.main
```

## Environment Variables

- `MONGO_URI`: MongoDB connection string
- `MONGO_DB`: MongoDB database name
- `KAFKA_BOOTSTRAP`: Kafka bootstrap servers
- `KAFKA_TOPIC_ANTI`: Antisemitic tweets topic
- `KAFKA_TOPIC_NOT_ANTI`: Non-antisemitic tweets topic

## Data Flow

1. **Retriever** reads from MongoDB → publishes to raw Kafka topics
2. **Preprocessor** consumes raw topics → cleans text → publishes to processed topics
3. **Enricher** consumes processed topics → adds sentiment/weapons → publishes to enriched topics
4. **Persister** consumes enriched topics → stores in MongoDB
5. **Data Retrieval** serves processed data via REST API