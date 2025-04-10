# BI Query Bot

A natural language to SQL query system that allows users to query sales data using plain English questions.

## Features

- Natural language processing using OpenAI API
- SQL query generation for SQLite database
- FastAPI backend for API endpoints
- Simple and efficient data querying

## Project Structure

```
bi_query_bot/
├── app/
│   ├── main.py           # FastAPI main application
│   ├── llm_agent.py      # OpenAI API integration
│   ├── db.py            # Database operations
│   ├── query_runner.py   # SQL query executor
│   └── templates/
│       └── prompt_template.txt  # LLM prompt template
├── data/
│   └── sales.db         # SQLite database
└── requirements.txt     # Project dependencies
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key in a .env file:
```
OPENAI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Usage

Send POST requests to `/query` endpoint with JSON body:
```json
{
    "question": "What was the total revenue last month?"
}
```

## Database Schema

Table: sales_data
- id (INTEGER PRIMARY KEY AUTOINCREMENT)
- product_name (TEXT)
- sales_date (DATE)
- sales_amount (INTEGER)
- revenue (FLOAT)

## License

MIT 