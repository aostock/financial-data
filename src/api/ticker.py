import yfinance as yf
import pandas as pd
from datetime import datetime, timezone
from src.common.cache import cache
from src.common.util import convert_list_dict_camel_to_snake, to_model
from src.common.finance_util import calculate_financial_metrics, calculate_income_stmt_missing, calculate_balance_sheet_missing, calculate_cash_flow_missing
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


@cache(timeout=60*60*24)
def get_ticker_info(symbol: str) -> TickerInfo:
    """
    获取 symbol 的信息
    :param symbol: symbol 名称
    :return: symbol 的信息
    """
    yf_ticker = yf.Ticker(symbol)
    data1 = yf_ticker.get_info()
    # Convert dict to TickerInfo model
    return to_model(data1, TickerInfo)


@cache(timeout=60*60)
def get_ticker_prices(symbol: str, interval: str, start_date: str, end_date: str) -> list[TickerPriceItem]:
    """
    获取 symbol 的价格数据
    :param symbol: symbol 名称
    :param interval: 时间间隔 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    :param start_date: 开始日期  2025-06-23
    :param end_date: 结束日期  2025-06-23
    :return: symbol 的价格数据
    """
    yf_ticker = yf.Ticker(symbol)
    data = yf_ticker.history(interval=interval, start=start_date, end=end_date, prepost=True)
    # 分组名称Date 修改
    data.index.name = 'date'
    # 表头命名修改
    data.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume', 'Dividends': 'dividends', 'Stock Splits': 'stock_splits'}, inplace=True)

    # convert  pd.DataFrame to list
    data = data.reset_index()
    data = data.to_dict(orient='records')
    # Convert list of dicts to TickerPriceItem models
    price_items = [to_model(item, TickerPriceItem) for item in data]
    return price_items

@cache(timeout=60*60)
def get_ticker_news(symbol: str, count=10) -> list[NewsItem]:
    """
    获取 symbol 的新闻数据
    :param symbol: symbol 名称
    :return: symbol 的新闻数据
    """
    yf_ticker = yf.Ticker(symbol)
    data = yf_ticker.get_news(count=count)
    # 只返回data list中的 content属性
    data = [item['content'] for item in data]
    convert_list_dict_camel_to_snake(data)
    # Convert list of dicts to NewsItem models
    news_items = [to_model(item, NewsItem) for item in data]
    return news_items


@cache(timeout=60*60*24)
def get_income_stmt(symbol: str, freq="yearly") -> list[IncomeStmtItem]:
    """
    获取 symbol 的分红数据
    :param symbol: symbol 名称
    :param freq: 时间间隔 "yearly" or "quarterly" or "trailing"
    :return: symbol 的分红数据
    """
    yf_ticker = yf.Ticker(symbol)
    data = yf_ticker.get_income_stmt(freq=freq, as_dict=True)
    # dict key to list, key attr name is date
    data = [{**item, 'date': key} for key, item in data.items()]
    convert_list_dict_camel_to_snake(data)
    # Convert list of dicts to IncomeStmtItem models
    income_stmt_items = [to_model(item, IncomeStmtItem) for item in data]
    for item in income_stmt_items:
        calculate_income_stmt_missing(item)
    return income_stmt_items


def get_balance_sheet(symbol: str, freq="yearly") -> list[BalanceSheetItem]:
    """
    获取 symbol 的资产负债表
    :param symbol: symbol 名称
    :param freq: 时间间隔 "yearly" or "quarterly" or "trailing"
    :return: symbol 的资产负债表
    """
    yf_ticker = yf.Ticker(symbol)
    data = yf_ticker.get_balance_sheet(freq=freq, as_dict=True)
    # dict key to list, key attr name is date
    data = [{**item, 'date': key} for key, item in data.items()]
    convert_list_dict_camel_to_snake(data)
    
    # Convert list of dicts to BalanceSheetItem models
    balance_sheet_items = [to_model(item, BalanceSheetItem) for item in data]
    for item in balance_sheet_items:
        calculate_balance_sheet_missing(item)
    return balance_sheet_items

def get_cash_flow(symbol: str, freq="yearly") -> list[CashFlowItem]:
    """
    获取 symbol 的现金流量表
    :param symbol: symbol 名称
    :param freq: 时间间隔 "yearly" or "quarterly" or "trailing"
    :return: symbol 的现金流量表
    """
    yf_ticker = yf.Ticker(symbol)
    data = yf_ticker.get_cash_flow(freq=freq, as_dict=True)
    # dict key to list, key attr name is date
    data = [{**item, 'date': key} for key, item in data.items()]
    convert_list_dict_camel_to_snake(data)
    
    # Convert list of dicts to CashFlowItem models
    cash_flow_items = [to_model(item, CashFlowItem) for item in data]
    for item in cash_flow_items:
        calculate_cash_flow_missing(item)
    return cash_flow_items


@cache(timeout=60*60*24)
def get_insider_transactions(symbol: str) -> list[InsiderTransactionItem]:
    """
    获取内部人交易数据
    :param symbol: ticker名称
    :return: 内部人交易数据列表
    """
    yf_ticker = yf.Ticker(symbol)
    data = yf_ticker.get_insider_transactions()
    # rename columns
    data.rename(columns={'Insider': 'insider', 'Position': 'position', 'Transaction': 'transaction', 'Start Date': 'startDate', 'Ownership': 'ownership'}, inplace=True)

    data = data.reset_index()
    data = data.to_dict(orient='records')
    # remove index attr
    data = [{k: v for k, v in item.items() if k != 'index'} for item in data]
    convert_list_dict_camel_to_snake(data)
    # Convert list of dicts to InsiderTransactionItem models
    insider_transaction_items = [to_model(item, InsiderTransactionItem) for item in data]
    return insider_transaction_items

@cache(timeout=60*60*24)
def get_insider_roster_holders(symbol: str) -> list[InsiderRosterHolderItem]:
    """
    获取内部人持股数据
    :param symbol: ticker名称
    :return: 内部人持股数据列表
    """
    yf_ticker = yf.Ticker(symbol)
    data = yf_ticker.get_insider_roster_holders()
    # rename columns
    data.rename(columns={'Name': 'name', 'Position': 'position', 'URL': 'url', 'Most Recent Transaction': 'mostRecentTransaction', 'Latest Transaction Date': 'latestTransactionDate', 'Shares Owned Directly': 'sharesOwnedDirectly', 'Position Direct Date': 'positionDirectDate', 'Shares Owned Indirectly': 'sharesOwnedIndirectly', 'Position Indirect Date': 'positionIndirectDate'}, inplace=True)
    data = data.reset_index()
    data = data.to_dict(orient='records')
    # remove index attr
    data = [{k: v for k, v in item.items() if k != 'index'} for item in data]
    convert_list_dict_camel_to_snake(data)
    # Convert list of dicts to InsiderRosterHolderItem models
    insider_roster_holder_items = [to_model(item, InsiderRosterHolderItem) for item in data]
    return insider_roster_holder_items


@cache(timeout=60*60)
def get_insider_purchases(symbol: str) -> list[InsiderPurchaseItem]:
    """
    获取内部人购买数据
    :param symbol: ticker名称
    :return: 内部人购买数据列表
    """
    yf_ticker = yf.Ticker(symbol)
    data = yf_ticker.get_insider_purchases()
    # rename columns
    data.rename(columns={'Insider Purchases Last 6m': 'insiderPurchasesLast6m', 'Shares': 'shares', 'Trans': 'trans'}, inplace=True)
    data = data.reset_index()
    data = data.to_dict(orient='records')
    # remove index attr
    data = [{k: v for k, v in item.items() if k != 'index'} for item in data]
    convert_list_dict_camel_to_snake(data)
    # Convert list of dicts to InsiderPurchaseItem models
    insider_purchase_items = [to_model(item, InsiderPurchaseItem) for item in data]
    return insider_purchase_items

@cache(timeout=60*60)
def get_financial_metrics(symbol: str, freq="yearly") -> list[FinancialMetricItem]:
    """
    获取 symbol 的财务指标数据
    :param symbol: symbol 名称
    :param freq: 时间间隔 "yearly" or "quarterly" or "trailing"
    :return: symbol 的财务指标数据
    """
    response = get_financial_items(symbol, None, freq)
    #  FinancialItem to FinancialMetricItem
    financial_metrics_items = [to_model(item.model_dump(), FinancialMetricItem) for item in response]
    return financial_metrics_items


def get_financial_items(symbol: str, items: list[str] = None, freq="yearly") -> list[FinancialItem]:
    """
    获取 symbol 的财务指标数据
    :param symbol: symbol 名称
    :param items: 财务指标列表, 如果为 None, 则返回 计算的财务指标
    :param freq: 时间间隔 "yearly" or "quarterly" or "trailing"
    :return: symbol 的财务指标数据
    """
    if items is not None and 'date' not in items:
        items.append('date')

    income_stmt_list = get_income_stmt(symbol, freq)
    balance_sheet_list = get_balance_sheet(symbol, freq)
    cash_flow_list = get_cash_flow(symbol, freq)

    # 检查 income_stmt_list， balance_sheet_list，cash_flow_list， 按 date 倒序
    income_stmt_list = sorted(income_stmt_list, key=lambda x: x.date, reverse=True)
    balance_sheet_list = sorted(balance_sheet_list, key=lambda x: x.date, reverse=True)
    cash_flow_list = sorted(cash_flow_list, key=lambda x: x.date, reverse=True)

    # 检查 income_stmt_list， balance_sheet_list，cash_flow_list 的长度是否一致, 相同年月的数据为一组, 同时存在于3者的才加入
    year_months = []
    for item in income_stmt_list:
        year_month = item.date.strftime('%Y-%m')
        if year_month not in year_months:
            year_months.append(year_month)
    balance_year_months = []
    for item in balance_sheet_list:
        year_month = item.date.strftime('%Y-%m')
        if year_month not in balance_year_months:
            balance_year_months.append(year_month)
    cash_year_months = []
    for item in cash_flow_list:
        year_month = item.date.strftime('%Y-%m')
        if year_month not in cash_year_months:
            cash_year_months.append(year_month)
    # 取交集
    year_months = list(set(year_months) & set(balance_year_months) & set(cash_year_months))
    income_stmt_list = [item for item in income_stmt_list if item.date.strftime('%Y-%m') in year_months]
    balance_sheet_list = [item for item in balance_sheet_list if item.date.strftime('%Y-%m') in year_months]
    cash_flow_list = [item for item in cash_flow_list if item.date.strftime('%Y-%m') in year_months]

    # 获取最大 date 和 最小 date
    max_date = None
    min_date = None
    if len(income_stmt_list) > 1:
        max_date = max(income_stmt_list[0].date, balance_sheet_list[0].date, cash_flow_list[0].date)
        min_date = min(income_stmt_list[-1].date, balance_sheet_list[-1].date, cash_flow_list[-1].date)
    else:
        max_date = income_stmt_list[0].date
        min_date = income_stmt_list[0].date
    # min_date 往前推1个月
    min_date = min_date - pd.DateOffset(months=1)
    # max_date min_date 格式转 str
    max_date = max_date.strftime('%Y-%m-%d')
    min_date = min_date.strftime('%Y-%m-%d')

    # prices 升序排列
    prices = get_ticker_prices(symbol, '1d', min_date, max_date)

    # 计算财务指标
    financial_items = []
    for i, income_stmt in enumerate(income_stmt_list):
        balance_sheet = balance_sheet_list[i]
        cash_flow = cash_flow_list[i]
        pre_index = i + 1 if i < len(income_stmt_list) - 1 else i
        pre_income_stmt = income_stmt_list[pre_index]
        pre_balance_sheet = balance_sheet_list[pre_index]
        pre_cash_flow = cash_flow_list[pre_index]

        date = income_stmt.date
        # get last date price in prices， 获取 date 之前的最近价格
        last_date_price = None
        for j, row in enumerate(prices):
            # Cannot compare tz-naive and tz-aware timestamps, convert to tz-naive
            row_date = row.date.replace(tzinfo=None)
            if row_date > date:
                if j > 0:
                    last_date_price = prices[j - 1]
                else:
                    last_date_price = row
                break
        if last_date_price is None:
            last_date_price = prices[-1]

        metrics = calculate_financial_metrics(last_date_price.close, income_stmt, balance_sheet, cash_flow, pre_income_stmt, pre_balance_sheet, pre_cash_flow)
        metrics['symbol'] = symbol
        if items is None:
            financial_items.append(metrics)
        else:
            metrics_items = [metrics, last_date_price.model_dump(), income_stmt.model_dump(), balance_sheet.model_dump(), cash_flow.model_dump()]
            financial_item = {}
            for item in items:
                for metrics_item in metrics_items:
                    if item in metrics_item:
                        financial_item[item] = metrics_item[item]
                        break
            financial_items.append(financial_item)
    
    # Convert list of dicts to FinancialMetricItem models
    financial_items = [to_model(item, FinancialItem) for item in financial_items]
    return financial_items

@cache(timeout=60*60)
def lookup_ticker(query: str) -> list[LookupItem]:
    """
    搜索 symbol 名称
    :param query: 搜索关键词
    :return: 搜索结果列表
    """
    data = yf.Lookup(query)
    stock_data = data.get_stock()
    stock_data = stock_data.to_dict(orient='index')
    # add key to object value
    stock_data = [{'symbol': k, **v} for k, v in stock_data.items()]
    convert_list_dict_camel_to_snake(stock_data)
    # 2025-07-23T08:47:33Z
    time_now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    for item in stock_data:
        item['time'] = time_now
    # Convert list of dicts to LookupItem models
    lookup_items = [to_model(item, LookupItem) for item in stock_data]
    return lookup_items
