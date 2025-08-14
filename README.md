# Financial Data Service

A FastAPI-based financial data service that provides comprehensive stock market information through RESTful APIs. The service uses Yahoo Finance (yfinance) as the primary data source to retrieve real-time stock information, prices, news, financial statements, and other related data.

This service serves as the data provider for the [financial-agents](https://github.com/aostock/financial-agents) project, supplying all the financial data needed for AI-powered financial analysis and trading agents.

## Project Overview

This service provides a unified API interface for accessing various types of financial data for stock tickers. It includes built-in caching mechanisms to improve performance and reduce external API calls, along with proper error handling and response formatting.

## Features

- **Ticker Information**: Company details, sector, industry, market cap, etc.
- **Stock Prices**: Historical price data with various time intervals
- **News**: Recent news articles related to specific tickers
- **Financial Statements**: Income statements, balance sheets, and cash flow statements
- **Insider Data**: Insider transactions, holdings, and purchases
- **Financial Metrics**: Key financial ratios and calculated metrics
- **Ticker Lookup**: Search functionality for finding ticker symbols

## API Endpoints

All API endpoints require authorization via the 'Authorization: Bearer <token>' header. The default token is 'secret-token' but can be overridden with the API_TOKEN environment variable.

### Core Endpoints

- `GET /api/v1/ticker/info` - Get ticker information
- `GET /api/v1/ticker/prices` - Get historical ticker prices
- `GET /api/v1/ticker/news` - Get recent news for a ticker
- `GET /api/v1/ticker/income_stmt` - Get income statement data
- `GET /api/v1/ticker/balance_sheet` - Get balance sheet data
- `GET /api/v1/ticker/cash_flow` - Get cash flow data
- `GET /api/v1/ticker/insider_transactions` - Get insider transactions
- `GET /api/v1/ticker/insider_roster_holders` - Get insider roster holders
- `GET /api/v1/ticker/insider_purchases` - Get insider purchases
- `GET /api/v1/ticker/financial_metrics` - Get financial metrics
- `GET /api/v1/ticker/financial_items` - Get specific financial items
- `GET /api/v1/ticker/lookup` - Lookup ticker symbols

### Test Endpoint

- `GET /api/v1/test` - Simple test endpoint

## Authentication

All endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer secret-token
```

The token can be customized using the `API_TOKEN` environment variable.

## Project Structure

```
financial-data/
├── main.py                 # FastAPI application and routing
├── src/
│   ├── api/                # Business logic for data fetching
│   ├── common/             # Utility functions and helpers
│   └── models/             # Pydantic data models
├── CLAUDE.md              # Claude Code instructions
└── README.md              # This file
```

## Business Logic

### Data Flow
1. API requests are received by FastAPI endpoints in `main.py`
2. Endpoints call functions in `src/api/ticker.py` to fetch data
3. Data is retrieved from Yahoo Finance using the `yfinance` library
4. Raw data is processed, transformed, and converted to Pydantic models
5. Responses are formatted using the `BaseResponse` wrapper with consistent structure

### Key Components

1. **Response Handling**: All API responses follow a consistent format using `BaseResponse` model with code, data, and message fields
2. **Data Conversion**: Utilities to convert between camelCase and snake_case naming conventions
3. **Caching**: Built-in caching mechanism using decorators to improve performance and reduce API calls
4. **Error Handling**: Centralized exception handling for consistent error responses
5. **Data Models**: Comprehensive Pydantic models for all financial data types

### Caching Strategy

- Ticker info: 24-hour cache
- Prices: 1-hour cache
- News: 1-hour cache
- Financial statements: 24-hour cache
- Insider data: 24-hour cache
- Financial metrics: 1-hour cache
- Ticker lookup: 1-hour cache

## Development Setup

### Prerequisites

- Python 3.12+
- `uv` package manager

### Installation

1. Create and activate virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

### Running the Application

Development mode:
```bash
source .venv/bin/activate
fastapi dev main.py
```

Production mode:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Environment Variables

- `API_TOKEN`: Custom authorization token (default: "secret-token")

## MCP Client Configuration

```json
{
  "mcpServers": {
    "finance-data": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://127.0.0.1:8000/mcp", "--header", "Authorization:Bearer secret-token"]
    }
  }
}
```