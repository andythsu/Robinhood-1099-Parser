import re
from typing import List
from pypdf import PdfReader
from tqdm import tqdm

from rh_1099.models.Transaction import Transaction

reporting_catagory_mapping = {
    "SHORT TERM TRANSACTIONS FOR COVERED TAX LOTS": "A",
    "LONG TERM TRANSACTIONS FOR COVERED TAX LOTS": "D"
}

def process_transactions(path) -> List[Transaction]:
    reader = PdfReader(path)
    number_of_pages = len(reader.pages)
    transactions: List[Transaction] = []
    for i in tqdm(range(0, number_of_pages)):
        page = reader.pages[i]
        text = page.extract_text()
        
        if "Proceeds from Broker and Barter Exchange Transactions" not in text: continue
            
        reporting_category = None
        for category, val in reporting_catagory_mapping.items():
            category_regex = re.compile(category, re.IGNORECASE)
            reporting_category = val if category_regex.search(text) else None
            if reporting_category is not None: break
        
        s = text.split("\n")
        
        prev_idx = -1
        symbols = (i for i, val in enumerate(s[prev_idx+1:]) if "Symbol:" in val and "CUSIP:" in val)
        while idx := next(symbols, len(s)):
            if prev_idx != -1:
                security = s[prev_idx]
                title = security.split("/")[0]
                lines = s[prev_idx+1:idx]
                # if last line is "security total" or "totals", we don't need to include it
                # this order is important as we start from the last line
                lines = ignore_lines("totals", lines)
                lines = ignore_lines("securitytotal", lines)
                transactions += parse_transactions(title, reporting_category, lines)
            prev_idx = idx
            if idx == len(s): break
    return transactions

def ignore_lines(keyword: str, lines: List[str]) -> List[str]:
    pattern = re.compile(keyword, re.IGNORECASE)
    return lines[:-1] if pattern.search(lines[-1]) else lines

def parse_transactions(title: str, reporting_category: str, lines: List[str]) -> List[Transaction]:
    transactions: List[Transaction] = []
    for _,val in enumerate(lines):
        # val[6] could be a W if the transaction is a wash sale loss disallowed.
        date_sold, _, proceeds, date_acquired, cost, adjustment_amount, is_adjusted, *_ = val.split(" ")
        
        transactions.append(
            Transaction(
                title,
                date_sold,
                date_acquired,
                proceeds,
                cost,
                adjustment_amount if is_adjusted == 'W' or is_adjusted == 'D' else None,
                is_adjusted == 'W',
                reporting_category,
                None,
            )
        )
    return transactions