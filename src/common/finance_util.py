import pandas as pd
import math
import numpy as np
from src.models.ticker_balance_sheet_model import BalanceSheetItem
from src.models.ticker_income_stmt_model import IncomeStmtItem
from src.models.ticker_cash_flow_model import CashFlowItem
from pydantic import BaseModel

def safe_divide(*kwargs):
    """安全除法"""
    for value in kwargs:
        if value is None or math.isnan(value):
            return None
    try:
        result = kwargs[0]
        for value in kwargs[1:]:
            if value is not None:
                result /= value
        return result
    except Exception:
        return None

def safe_subtract(*kwargs):
    """安全减法"""
    result = 0
    if kwargs[0] is not None:
        result = kwargs[0]
    for value in kwargs[1:]:
        if value is not None and not math.isnan(value):
            result -= value
    return result

def safe_add(*kwargs):
    """安全加法"""
    result = 0
    for value in kwargs:
        if value is not None and not math.isnan(value):
            result += value
    return result

def safe_multiply(*kwargs):
    """安全乘法"""
    result = 1
    for value in kwargs:
        if value is not None and not math.isnan(value):
            result *= value
    return result

def check_missing_keys(data: BaseModel, required_keys, dict_name):
    """检查字段缺失"""
    missing = [key for key in required_keys if key not in data.model_dump()]
    if missing:
        print(f"{dict_name}_not_exist_keys: {missing}")
    return missing

def calculate_financial_metrics(
    price: float,
    income_stmt: IncomeStmtItem,
    balance_sheet: BalanceSheetItem,
    cash_flow: CashFlowItem,
    pre_income_stmt: IncomeStmtItem,
    pre_balance_sheet: BalanceSheetItem,
    pre_cash_flow: CashFlowItem
):
    # 字段校验
    check_missing_keys(income_stmt, ["date", "net_income", "total_revenue", "gross_profit", "operating_income",
                                   "ebitda", "diluted_average_shares"], "income_stmt")
    check_missing_keys(balance_sheet, ["stockholders_equity", "total_assets", "invested_capital", 
                                     "current_assets", "current_liabilities", "accounts_receivable", 
                                     "inventory", "working_capital", "total_debt", "net_debt"], "balance_sheet")
    check_missing_keys(cash_flow, ["free_cash_flow", "operating_cash_flow"], "cash_flow")

    # 初始化结果字典
    ratios = {"date": income_stmt.date}

    # 市值相关
    market_cap = safe_multiply(price, income_stmt.diluted_average_shares)
    enterprise_value = safe_add(market_cap, balance_sheet.net_debt)
    ratios.update({
        "market_cap": market_cap,
        "enterprise_value": enterprise_value
    })

    # 资产负债表相关
    # 融资现金流 = 债务融资 + 股东分配 + 其他
    ratios.update({
        "dividends_and_other_cash_distributions": safe_subtract(cash_flow.financing_cash_flow,
            cash_flow.net_issuance_payments_of_debt,
            cash_flow.net_other_financing_charges),
        "issuance_or_purchase_of_equity_shares": safe_subtract(cash_flow.financing_cash_flow,
            cash_flow.net_issuance_payments_of_debt,
            cash_flow.cash_dividends_paid,
            cash_flow.net_other_financing_charges)
    })

    # 基础比率
    pe = safe_divide(price, income_stmt.diluted_eps)
    earnings_growth = safe_divide(
            safe_subtract(income_stmt.net_income, pre_income_stmt.net_income), 
            pre_income_stmt.net_income
        )
    ratios.update({
        "price_to_earnings_ratio": pe,
        "price_to_book_ratio": safe_divide(market_cap, balance_sheet.stockholders_equity),
        "price_to_sales_ratio": safe_divide(market_cap, income_stmt.total_revenue),
        "enterprise_value_to_ebitda_ratio": safe_divide(enterprise_value, income_stmt.ebitda),
        "enterprise_value_to_revenue_ratio": safe_divide(enterprise_value, income_stmt.total_revenue),
        "free_cash_flow_yield": safe_divide(cash_flow.free_cash_flow, market_cap),
        "peg_ratio": safe_divide(pe, earnings_growth)
    })
    
    # 利润率
    ratios.update({
        "gross_margin": safe_divide(income_stmt.gross_profit, income_stmt.total_revenue),
        "operating_margin": safe_divide(income_stmt.operating_income, income_stmt.total_revenue),
        "net_margin": safe_divide(income_stmt.net_income, income_stmt.total_revenue)
    })
    
    # ROE/ROA/ROIC
    ratios.update({
        "return_on_equity": safe_divide(income_stmt.net_income, balance_sheet.stockholders_equity),
        "return_on_assets": safe_divide(income_stmt.net_income, balance_sheet.total_assets),
        "return_on_invested_capital": safe_divide(income_stmt.net_income, balance_sheet.invested_capital)
    })
    
    # 运营效率
    ratios.update({
        "asset_turnover": safe_divide(income_stmt.total_revenue, balance_sheet.total_assets),
        "inventory_turnover": safe_divide(income_stmt.total_revenue, balance_sheet.inventory),
        "receivables_turnover": safe_divide(income_stmt.total_revenue, balance_sheet.accounts_receivable),
        "days_sales_outstanding": safe_divide(365, safe_divide(income_stmt.total_revenue, balance_sheet.accounts_receivable)),
        "operating_cycle": safe_add(
            safe_divide(365, safe_divide(income_stmt.total_revenue, balance_sheet.inventory)),
            safe_divide(365, safe_divide(income_stmt.total_revenue, balance_sheet.accounts_receivable))
        ),
        "working_capital_turnover": safe_divide(income_stmt.total_revenue, balance_sheet.working_capital)
    })
    
    # 流动性比率
    ratios.update({
        "current_ratio": safe_divide(balance_sheet.current_assets, balance_sheet.current_liabilities),
        "quick_ratio": safe_divide(
            safe_subtract(balance_sheet.current_assets, balance_sheet.inventory), 
            balance_sheet.current_liabilities
        ),
        "cash_ratio": safe_divide(balance_sheet.cash_and_cash_equivalents, balance_sheet.current_liabilities),
        "operating_cash_flow_ratio": safe_divide(cash_flow.operating_cash_flow, balance_sheet.current_liabilities)
    })
    
    # 杠杆比率
    ratios.update({
        "debt_to_equity": safe_divide(balance_sheet.total_debt, balance_sheet.stockholders_equity),
        "debt_to_assets": safe_divide(balance_sheet.total_debt, balance_sheet.total_assets),
        "interest_coverage": safe_divide(income_stmt.ebitda, income_stmt.interest_expense)
    })
    
    # 成长性指标
    ratios.update({
        "revenue_growth": safe_divide(
            safe_subtract(income_stmt.total_revenue, pre_income_stmt.total_revenue), 
            pre_income_stmt.total_revenue
        ),
        "book_value_growth": safe_divide(
            safe_subtract(balance_sheet.stockholders_equity, pre_balance_sheet.stockholders_equity), 
            pre_balance_sheet.stockholders_equity
        ),
        "earnings_per_share_growth": safe_divide(
            safe_subtract(income_stmt.diluted_eps, pre_income_stmt.diluted_eps), 
            pre_income_stmt.diluted_eps
        ),
        "free_cash_flow_growth": safe_divide(
            safe_subtract(cash_flow.free_cash_flow, pre_cash_flow.free_cash_flow), 
            pre_cash_flow.free_cash_flow
        ),
        "operating_income_growth": safe_divide(
            safe_subtract(income_stmt.operating_income, pre_income_stmt.operating_income), 
            pre_income_stmt.operating_income
        ),
        "ebitda_growth": safe_divide(
            safe_subtract(income_stmt.ebitda, pre_income_stmt.ebitda), 
            pre_income_stmt.ebitda
        )
    })
    
    # 收益质量
    ratios.update({
        "payout_ratio": safe_divide(cash_flow.cash_dividends_paid, income_stmt.net_income),
        "earnings_per_share": income_stmt.diluted_eps,
        "book_value_per_share": safe_divide(balance_sheet.stockholders_equity, income_stmt.diluted_average_shares),
        "free_cash_flow_per_share": safe_divide(cash_flow.free_cash_flow, income_stmt.diluted_average_shares)
    })
    
    return ratios


def calculate_income_stmt_missing(income_stmt:IncomeStmtItem):
    calculated_values = {}

    # 按照依赖关系排序计算
    # 1. cost_of_revenue 或 gross_profit (基础计算)
    if income_stmt.gross_profit is None:
        total_revenue = income_stmt.total_revenue
        cost_of_revenue = income_stmt.cost_of_revenue
        if total_revenue is not None and cost_of_revenue is not None:
            calculated_values['gross_profit'] = total_revenue - cost_of_revenue
    
    if income_stmt.cost_of_revenue is None:
        total_revenue = income_stmt.total_revenue
        gross_profit = income_stmt.gross_profit or calculated_values.get('gross_profit')
        if total_revenue is not None and gross_profit is not None:
            calculated_values['cost_of_revenue'] = total_revenue - gross_profit

    # 2. operating_income (依赖 gross_profit)
    if income_stmt.operating_income is None:
        gross_profit = income_stmt.gross_profit or calculated_values.get('gross_profit')
        operating_expense = income_stmt.operating_expense
        if gross_profit is not None and operating_expense is not None:
            calculated_values['operating_income'] = gross_profit - operating_expense

    # 3. ebit (依赖 operating_income)
    if income_stmt.ebit is None:
        operating_income = income_stmt.operating_income or calculated_values.get('operating_income')
        other_income_expense = income_stmt.other_income_expense
        if operating_income is not None:
            calculated_values['ebit'] = operating_income + other_income_expense

    # 4. ebitda (依赖 ebit)
    if income_stmt.ebitda is None:
        ebit = income_stmt.ebit or calculated_values.get('ebit')
        depreciation = income_stmt.reconciled_depreciation
        if ebit is not None and depreciation is not None:
            calculated_values['ebitda'] = ebit + depreciation

    # 更新原始对象
    target_keys = ['gross_profit', 'operating_income', 'ebit', 'ebitda', 'cost_of_revenue']
    for key, value in calculated_values.items():
        if key in target_keys:
            setattr(income_stmt, key, value)

    return {k: v for k, v in calculated_values.items() if k in target_keys}


def calculate_balance_sheet_missing(balance_sheet:BalanceSheetItem):
    calculated_values = {}

    # 按照依赖关系排序计算
    # 1. net_debt (独立计算)
    if balance_sheet.net_debt is None:
        total_debt = balance_sheet.total_debt
        cash = balance_sheet.cash_and_cash_equivalents
        if total_debt is not None and cash is not None:
            calculated_values['net_debt'] = total_debt - cash

    # 2. current_liabilities (独立估算)
    if balance_sheet.current_liabilities is None:
        payables = balance_sheet.payables
        tax_payable = balance_sheet.total_tax_payable
        other_payable = balance_sheet.other_payable
        calculated_values['current_liabilities'] = safe_add(payables, tax_payable, other_payable)

    # 3. current_assets (独立估算)
    if balance_sheet.current_assets is None:
        cash = balance_sheet.cash_and_cash_equivalents
        investments = balance_sheet.investmentin_financial_assets
        if cash is not None:
            calculated_values['current_assets'] = cash + investments * 0.3

    # 4. accounts_receivable (独立估算)
    if balance_sheet.accounts_receivable is None:
        total_assets = balance_sheet.total_assets
        if total_assets is not None:
            calculated_values['accounts_receivable'] = total_assets * 0.075

    # 5. inventory (独立估算)
    if balance_sheet.inventory is None:
        total_assets = balance_sheet.total_assets
        if total_assets is not None:
            calculated_values['inventory'] = total_assets * 0.02

    # 6. working_capital (依赖 current_assets 和 current_liabilities)
    if balance_sheet.working_capital is None:
        current_assets = balance_sheet.current_assets or calculated_values.get('current_assets')
        current_liabilities = balance_sheet.current_liabilities or calculated_values.get('current_liabilities')
        if current_assets is not None and current_liabilities is not None:
            calculated_values['working_capital'] = current_assets - current_liabilities

    # 更新原始对象
    target_keys = ['net_debt', 'current_assets', 'current_liabilities', 'accounts_receivable', 'inventory', 'working_capital']
    for key, value in calculated_values.items():
        if key in target_keys:
            setattr(balance_sheet, key, value)

    return {k: v for k, v in calculated_values.items() if k in target_keys}


def calculate_cash_flow_missing(cash_flow:CashFlowItem):
    calculated_values = {}

    # common_stock_dividend_paid ≈ cash_dividends_paid
    if cash_flow.common_stock_dividend_paid is None:
        dividends_paid = cash_flow.cash_dividends_paid
        if dividends_paid is not None:
            calculated_values['common_stock_dividend_paid'] = dividends_paid

    # 更新原始对象
    target_keys = ['common_stock_dividend_paid']
    for key, value in calculated_values.items():
        if key in target_keys:
            setattr(cash_flow, key, value)

    return {k: v for k, v in calculated_values.items() if k in target_keys}

if __name__ == '__main__':
    # Test code would need to import the model classes and create instances
    # This is just a placeholder to show the structure
    pass
