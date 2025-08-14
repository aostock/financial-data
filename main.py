from dotenv import load_dotenv
import os
load_dotenv()

from typing import Optional
from fastapi import FastAPI, Query, Header, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP
from src.common.fastapi_util import success, exception_handler, BaseResponse
from src.api.ticker import get_ticker_info, get_ticker_prices, get_ticker_news, get_income_stmt, get_balance_sheet, get_cash_flow, get_insider_transactions, get_insider_roster_holders, get_insider_purchases, get_financial_metrics, lookup_ticker, get_financial_items
from src.models.ticker_info_model import TickerInfo
from src.models.ticker_prices_model import TickerPriceItem
from src.models.ticker_news_model import NewsItem
from src.models.ticker_income_stmt_model import IncomeStmtItem
from src.models.ticker_balance_sheet_model import BalanceSheetItem
from src.models.ticker_cash_flow_model import CashFlowItem
from src.models.ticker_insider_transactions_model import InsiderTransactionItem
from src.models.ticker_insider_roster_holders_model import InsiderRosterHolderItem
from src.models.ticker_insider_purchases_model import InsiderPurchaseItem
from src.models.ticker_financial_metrics_model import FinancialMetricItem
from src.models.ticker_financial_items_model import FinancialItem
from src.models.ticker_lookup_model import LookupItem
import uvicorn


# Get the valid token from environment variable or use default
VALID_TOKEN = os.getenv("API_TOKEN", "secret-token")

async def verify_token(authorization: str = Header(None),
                       authentication: str = Header(None),
                       x_api_key: str = Header(None),
                       api_key: str = Header(None),
                       x_token: str = Header(None),
                       token: str = Header(None),
                       request: Request = None):
    """Verify the authorization token from the request header"""
    # Skip authorization for MCP routes and docs
    if request and (request.url.path.startswith("/mcp") or 
                    request.url.path.startswith("/sse") or
                    request.url.path.startswith("/docs") or 
                    request.url.path.startswith("/redoc") or 
                    request.url.path.startswith("/openapi.json")):
        return True
    auth_str = authorization or authentication or x_api_key or api_key or x_token or token
    if not auth_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token",
        )
    
    # Check if token is valid (format: "Bearer <token>")
    try:
        token_type, token = auth_str.split(" ")
        if token_type != "Bearer" or token != VALID_TOKEN:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization token",
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )
    
    return True


app = FastAPI(title="Aostock financial data API", version="1.0", description="Aostock financial data API. All API endpoints require authorization via the 'Authorization: Bearer <token>' header. The default token is 'secret-token' but can be overridden with the API_TOKEN environment variable.", dependencies=[Depends(verify_token)])

# Add CORS middleware for remote access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def general_exception_handler(request, e: Exception):
    """Global exception handler for the FastAPI application.
    
    Args:
        request: The incoming request object
        e: The exception that was raised
        
    Returns:
        A standardized error response
    """
    return exception_handler(request, e)


@app.get("/api/v1/test", operation_id="get_test", tags=["Test"], summary="Test", description="Test endpoint", response_model=BaseResponse)
async def test():
    """Test endpoint that returns a simple message."""
    return success("Hello World")


@app.get("/api/v1/ticker/info", operation_id="get_ticker_info", tags=["Ticker"], summary="Ticker Info",
description="Get ticker info",
response_model=BaseResponse[TickerInfo])
async def ticker_info(symbol: str = Query(..., description="Ticker symbols, eg: AAPL, 601398.SS")):
    """Get information about a specific ticker symbol.
    
    Args:
        symbol: The ticker symbol to get information for (e.g., AAPL, 601398.SS)
        
    Returns:
        Ticker information including company name, sector, industry, etc.
    """
    data = get_ticker_info(symbol)
    return success(data)


@app.get("/api/v1/ticker/prices", operation_id="get_ticker_prices", tags=["Ticker"], summary="Ticker Prices",
    description="Get ticker prices",
    response_model=BaseResponse[list[TickerPriceItem]])
async def ticker_prices(symbol: str = Query(..., description="Ticker symbols, eg: AAPL, 601398.SS"),
    interval: str = Query(..., description="Time interval, eg: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo"),
    start_date: str = Query(..., description="Start date, eg: 2025-06-23"),
    end_date: str = Query(..., description="End date, eg: 2025-06-23")):
    """Get historical prices for a specific ticker symbol.
    
    Args:
        symbol: The ticker symbol to get prices for (e.g., AAPL, 601398.SS)
        interval: Time interval for the data (e.g., 1m, 1h, 1d)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        List of ticker price items for the specified period
    """
    data = get_ticker_prices(symbol, interval, start_date, end_date)
    return success(data)


@app.get("/api/v1/ticker/news", operation_id="get_ticker_news", tags=["Ticker"], summary="Ticker News",
description="Get ticker news",
response_model=BaseResponse[list[NewsItem]])
async def ticker_news(symbol: str = Query(..., description="Ticker symbols, eg: AAPL, 601398.SS"),
    count: Optional[int] = Query(default=10, description="Number of news, eg: 10")):
    """Get recent news articles for a specific ticker symbol.
    
    Args:
        symbol: The ticker symbol to get news for (e.g., AAPL, 601398.SS)
        count: Number of news articles to retrieve (default: 10)
        
    Returns:
        List of news items related to the specified ticker
    """
    data = get_ticker_news(symbol, count)
    return success(data)


@app.get("/api/v1/ticker/income_stmt", operation_id="get_ticker_income_stmt", tags=["Ticker"], summary="Ticker Income Statement",
description="Get ticker income statement",
response_model=BaseResponse[list[IncomeStmtItem]])
async def ticker_income_stmt(symbol: str = Query(..., description="Ticker symbols, eg: AAPL, 601398.SS"),
    freq: str = Query(default='yearly', description="Income statement frequency, eg: yearly, quarterly or trailing")):
    """Get income statement data for a specific ticker symbol.
    
    Args:
        symbol: The ticker symbol to get income statement for (e.g., AAPL, 601398.SS)
        freq: Frequency of data - 'yearly', 'quarterly', or 'trailing' (default: yearly)
        
    Returns:
        List of income statement items for the specified ticker
    """
    data = get_income_stmt(symbol, freq)
    return success(data)


@app.get("/api/v1/ticker/balance_sheet", operation_id="get_ticker_balance_sheet", tags=["Ticker"], summary="Ticker Balance Sheet",
description="Get ticker balance sheet",
response_model=BaseResponse[list[BalanceSheetItem]])
async def ticker_balance_sheet(symbol: str = Query(..., description="Ticker symbols, eg: AAPL, 601398.SS"),
    freq: str = Query(default='yearly', description="Balance sheet frequency, eg: yearly, quarterly or trailing")):
    """Get balance sheet data for a specific ticker symbol.
    
    Args:
        symbol: The ticker symbol to get balance sheet for (e.g., AAPL, 601398.SS)
        freq: Frequency of data - 'yearly', 'quarterly', or 'trailing' (default: yearly)
        
    Returns:
        List of balance sheet items for the specified ticker
    """
    data = get_balance_sheet(symbol, freq)
    return success(data)


@app.get("/api/v1/ticker/cash_flow", operation_id="get_ticker_cash_flow", tags=["Ticker"], summary="Ticker Cash Flow",
description="Get ticker cash flow",
response_model=BaseResponse[list[CashFlowItem]])
async def ticker_cash_flow(symbol: str = Query(..., description="Ticker symbols, eg: AAPL, 601398.SS"),
    freq: str = Query(default='yearly', description="Cash flow frequency, eg: yearly, quarterly or trailing")):
    """Get cash flow data for a specific ticker symbol.
    
    Args:
        symbol: The ticker symbol to get cash flow for (e.g., AAPL, 601398.SS)
        freq: Frequency of data - 'yearly', 'quarterly', or 'trailing' (default: yearly)
        
    Returns:
        List of cash flow items for the specified ticker
    """
    data = get_cash_flow(symbol, freq)
    return success(data)


@app.get("/api/v1/ticker/insider_transactions", operation_id="get_ticker_insider_transactions", tags=["Ticker"], summary="Ticker Insider Transactions",
description="Get ticker insider transactions",
response_model=BaseResponse[list[InsiderTransactionItem]])
async def ticker_insider_transactions(symbol: str = Query(..., description="Ticker symbols, eg: AAPL, 601398.SS")):
    """Get insider transactions data for a specific ticker symbol.
    
    Args:
        symbol: The ticker symbol to get insider transactions for (e.g., AAPL, 601398.SS)
        
    Returns:
        List of insider transaction items for the specified ticker
    """
    data = get_insider_transactions(symbol)
    return success(data)

@app.get("/api/v1/ticker/insider_roster_holders", operation_id="get_ticker_insider_roster_holders", tags=["Ticker"], summary="Ticker Insider Roster Holders",
description="Get ticker insider roster holders",
response_model=BaseResponse[list[InsiderRosterHolderItem]])
async def ticker_insider_roster_holders(symbol: str = Query(..., description="Ticker symbols, eg: AAPL, 601398.SS")):
    """Get insider roster holders data for a specific ticker symbol.
    
    Args:
        symbol: The ticker symbol to get insider roster holders for (e.g., AAPL, 601398.SS)
        
    Returns:
        List of insider roster holder items for the specified ticker
    """
    data = get_insider_roster_holders(symbol)
    return success(data)

@app.get("/api/v1/ticker/insider_purchases", operation_id="get_ticker_insider_purchases", tags=["Ticker"], summary="Ticker Insider Purchases",
description="Get ticker insider purchases",
response_model=BaseResponse[list[InsiderPurchaseItem]])
async def ticker_insider_purchases(symbol: str = Query(..., description="Ticker symbols, eg: AAPL, 601398.SS")):
    """Get insider purchases data for a specific ticker symbol.
    
    Args:
        symbol: The ticker symbol to get insider purchases for (e.g., AAPL, 601398.SS)
        
    Returns:
        List of insider purchase items for the specified ticker
    """
    data = get_insider_purchases(symbol)
    return success(data)


@app.get("/api/v1/ticker/financial_metrics", operation_id="get_ticker_financial_metrics", tags=["Ticker"], summary="Ticker Financial Metrics",
description="Get ticker financial metrics",
response_model=BaseResponse[list[FinancialMetricItem]])
async def ticker_financial_metrics(symbol: str = Query(..., description="Ticker symbols, eg: AAPL, 601398.SS"), freq: Optional[str] = Query(default='yearly', description="Financial metrics frequency, eg: yearly, quarterly")):
    """Get financial metrics data for a specific ticker symbol.
    
    Args:
        symbol: The ticker symbol to get financial metrics for (e.g., AAPL, 601398.SS)
        freq: Frequency of data - 'yearly' or 'quarterly' (default: yearly)
        
    Returns:
        List of financial metric items for the specified ticker
    """
    data = get_financial_metrics(symbol, freq)
    return success(data)


@app.get("/api/v1/ticker/financial_items", operation_id="get_ticker_financial_items", tags=["Ticker"], summary="Ticker Financial Items",
description="Get ticker financial items",
response_model=BaseResponse[list[FinancialItem]])
async def ticker_financial_items(symbol: str = Query(..., description="Ticker symbols, eg: AAPL, 601398.SS"), items: Optional[str] = Query(default=None, description="Financial items, eg: revenue_growth,market_cap"), freq: Optional[str] = Query(default='yearly', description="Financial items frequency, eg: yearly, quarterly")):
    """Get specific financial items data for a ticker symbol.
    
    Args:
        symbol: The ticker symbol to get financial items for (e.g., AAPL, 601398.SS)
        items: Comma-separated list of specific financial items to retrieve
        freq: Frequency of data - 'yearly' or 'quarterly' (default: yearly)
        
    Returns:
        List of financial items for the specified ticker
    """
    if items is not None:
        items = items.split(',')
    data = get_financial_items(symbol, items, freq)
    return success(data)




@app.get("/api/v1/ticker/lookup", operation_id="get_ticker_lookup", tags=["Ticker"], summary="Ticker lookup",
description="lookup ticker",
response_model=BaseResponse[list[LookupItem]])
async def ticker_lookup(query: str = Query(..., description="lookup query, eg: AAPL")):
    """Look up ticker symbols based on a search query.
    
    Args:
        query: The search query to look up ticker symbols for (e.g., AAPL)
        
    Returns:
        List of matching ticker symbols and company names
    """
    data = lookup_ticker(query)
    return success(data)



mcp = FastApiMCP(app, describe_all_responses=True, headers=["authorization", "authentication", "x-api-key", "api-key", "x-token", "token"])
mcp.mount_http()
mcp.mount_sse()

if __name__ == "__main__":
    import uvicorn
    port = int( os.environ.get("PM2_SERVE_PORT", 8000))
    print(f"Starting FastAPI app with MCP on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
