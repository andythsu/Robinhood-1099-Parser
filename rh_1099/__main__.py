import argparse
import os
import os.path
from typing import List

from .models.Transaction import Transaction
from .pdf_parser.output import output_to_csv

from .pdf_parser.parser_2024 import (
    process_transactions
)


def is_valid_file(parser: argparse.ArgumentParser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def main():
    parser = argparse.ArgumentParser(
        prog='rh_1099',
        description='Robinhood Securities 1099 Tax Document Parser')
    parser.add_argument('--pdf', required=True, dest='pdf_path',
                        help='Input path to the 1099 PDF document', metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument('--csv', metavar="FILE", help='Output path of the parsed CSV')
    parser.add_argument('--silent', action='store_true', help='Hide progress bar')
    parser.add_argument('--check', action='store_true', help='Print total values to check')

    args = parser.parse_args()
    if not args.csv:
        args.csv = 'output.csv'

    transactions: List[Transaction] = []
    transactions = process_transactions(args.pdf_path)
    
    print(transactions)
    
    output_to_csv(transactions)
    
    # parser = Parser2020(args.pdf_path)
    # contents = parser.process(not args.silent)


    # Print values to crosscheck with PDF
    # if args.check:
    #     proceeds = contents.total("proceeds")
    #     cost = contents.total("cost")
    #     wash_sales_loss = contents.total("wash_sales_loss")
    #     gain_loss = contents.total("gain_loss")

    #     print(">>> Calculated Totals:")
    #     print("    Make sure the values matches with the PDF totals!")
    #     print(f"    proceeds: {proceeds:.2f}, cost: {cost:.2f}, wash_sales_loss: {wash_sales_loss:.2f}, gain_loss: {gain_loss:.2f}")


    # # Save as csv file
    # if not contents.empty():
    #     contents.to_csv(args.csv)
    #     print(f">>> Saved to {args.csv}")
    # else:
    #     print(f">>> No data to save to a file")

if __name__ == "__main__":
    main()