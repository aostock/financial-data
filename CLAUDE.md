# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based financial data service that provides stock market information through RESTful APIs. The service uses Yahoo Finance (yfinance) as the primary data source to retrieve stock information, prices, news, financial statements, and other related data.

## Code Architecture

1. **Main Application**: `main.py` - Contains all the API endpoints and FastAPI application setup
2. **API Layer**: `src/api/` - Contains the business logic for fetching and processing financial data
3. **Models**: `src/models/` - Pydantic models that define the structure of API responses
4. **Common Utilities**: `src/common/` - Utility functions for caching, data conversion, and FastAPI response handling
5. **Data Source**: Uses Yahoo Finance (yfinance) library to fetch real-time financial data

## Common Development Commands

### Running the Application

```bash
source .venv/bin/activate
fastapi dev main.py
```

### Dependencies

Dependencies are managed using `uv` (as indicated by `pyproject.toml` and `uv.lock`):

- Python version: >=3.12
- Main dependencies: fastapi, yfinance, financetoolkit, dotenv

## API Structure

The API provides endpoints for:

- Ticker information (`/api/v1/ticker/info`)
- Stock prices (`/api/v1/ticker/prices`)
- News (`/api/v1/ticker/news`)
- Financial statements (income statement, balance sheet, cash flow)
- Insider transactions and holdings
- Financial metrics and calculations
- Ticker lookup/search functionality

## Key Components

1. **Response Handling**: All API responses follow a consistent format using `BaseResponse` model with code, data, and message fields
2. **Data Conversion**: Utilities to convert between camelCase and snake_case naming conventions
3. **Caching**: Built-in caching mechanism to improve performance and reduce API calls
4. **Error Handling**: Centralized exception handling for consistent error responses
5. **Data Models**: Comprehensive Pydantic models for all financial data types

## Testing

Testing can be done by running `test.py` which contains example usage of the API functions and data fetching utilities.
