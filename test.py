import yfinance as yf
import json
import os
from fastapi.encoders import jsonable_encoder
from src.api.ticker import get_income_stmt, get_balance_sheet, get_cash_flow, get_ticker_prices

# 获取港股市场信息

def get_hk_markets():
    # 获取所有港股市场
    hk_market = yf.Market('HK')
    # 打印所有港股市场
    print(hk_market.summary)

def get_prices(symbol, interval, interval_multiplier, start_date, end_date, limit=10000):
    # 获取所有港股市场
    hk_market = yf.Ticker(symbol)
    # 打印所有港股市场
    print(hk_market)


def save_to_json_file(data, file_path):
    
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w') as f:
        json.dump(jsonable_encoder(data), f)

if __name__ == '__main__':
    # code = '601398.SS'
    # Apple 公司股票代码
    code = 'AAPL'
    ticker = yf.Ticker(code)
    # 获取 Apple 公司的历史股票价格  Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    # Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    interval = '1d'
    start_date = '2024-06-01'
    end_date = '2025-07-13'
    freq = 'yearly'

    query = 'BANK of china'
    data = yf.Search(query).all
    save_to_json_file(data, f'csv/test/search_{query}.json')

    # data.to_csv(f'csv/test/search_{query}.csv')
    # data = yf.download("AAPL", start="2017-01-01", end="2017-04-30")
    # save DataFrame to csv
    # data.to_csv(f'csv/test/{code}/download.csv')

    # save_to_json_file(data, f'csv/test/{code}/download.json')
    # save_to_json_file(symbol.info, f'csv/test/{code}/info.json')

    # print('info', ticker.info)
    # print('shares', ticker.financials)
    # print('market_cap', ticker.fast_info.get('market_cap'))

    # get ticker prices
    # growth_estimates:list = ticker.get_growth_estimates(as_dict=True)
    # # save list data to json file
    # save_to_json_file(growth_estimates, f'csv/test/{code}/growth_estimates.json')

    # # 计算每日收盘价的平均值
    # average_close_price = sum([item['close'] for item in ticker_prices]) / len(ticker_prices)
    # print(f"每日收盘价的平均值为: {average_close_price}")

    # dataset : cap: 3463350367230, "weighted_average_shares": 15343783000, "weighted_average_shares_diluted": 15408095000   price : 227.79

    # market_cap = 14935799808 * 226.99208068847656
    # print(f"市场总市值为: {market_cap}")

    # print('自己计算价格', 3153843453952 / 14935799808)

    # print('dataset 计算价格1', 3463350367230 /14935826000 )
    # print('dataset 计算价格2', 3463350367230 /15408095000 )  # 14935826000

    # # get income stmt
    # income_stmt = get_income_stmt(code, freq)
    # save_to_json_file(income_stmt, f'csv/test/{code}/income_stmt.json')

    # # get balance sheet
    # balance_sheet = get_balance_sheet(code, freq)
    # save_to_json_file(balance_sheet, f'csv/test/{code}/balance_sheet.json')

    # # get cash flow
    # cash_flow = get_cash_flow(code, freq)
    # save_to_json_file(cash_flow, f'csv/test/{code}/cash_flow.json')

    

    # 获取最新的价格
    # data1 = ticker.h

    # data2 = ticker.get_fast_info()
    # print(data2)
    