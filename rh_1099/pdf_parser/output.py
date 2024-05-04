import csv
from typing import List

from rh_1099.models.Transaction import Transaction

def output_to_csv(transactions: List[Transaction]):
    with open('output.csv', 'w', newline='') as csv_file:
        transactions = [t.to_dict() for t in transactions]
        w = csv.DictWriter(csv_file, transactions[0].keys())
        w.writeheader()
        w.writerows(transactions)