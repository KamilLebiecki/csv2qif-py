import csv
import argparse
from datetime import datetime
from typing import Any


def print_row(rowNr: Any, date: Any, amount: Any, payee: Any, family: Any, category: Any) -> None:
    """Pretty-print a single CSV row to the console."""
    print(
        f"{str(rowNr):<3} | "
        f"{str(date):<11} | "  # DD.MM'YYYY is 10 chars, using 11 for padding
        f"{str(amount):>12} | "
        f"{str(payee):<20} | "
        f"{str(family):<15} | "
        f"{str(category):<30}"
    )


def _normalize_amount(raw: str) -> str:
    """Normalize amount text for QIF: remove thousands separators and use dot as decimal."""
    s = raw.strip().replace(' ', '')
    # If there's both comma and dot, assume comma is thousands sep; remove commas
    if ',' in s and '.' in s:
        s = s.replace(',', '')
    # If only comma present, treat as decimal separator
    elif ',' in s and '.' not in s:
        s = s.replace(',', '.')
    return s


def csv2qif(input_file: str = 'input.csv', output_file: str = 'output.qif') -> None:
    """
    Convert a semicolon-delimited CSV to a QIF file.

    Expected CSV columns (in order):
    0: Date              (format: DD.MM.YYYY)
    1: Transaction       (signed number, e.g., -166.60)
    2: Payee             (e.g., Bank Alior)
    3: Family members    (may be empty; if present, append to Category with a leading '/')
    4: Category          (always present; may include brackets or colons)
    """
    qif_data = ["!Type:Bank"]

    try:
        with open(input_file, 'r', encoding='utf-8-sig', newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=';', skipinitialspace=True)
            rows = list(reader)
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_file}")
        return

    if not rows:
        print("Error: CSV is empty.")
        return

    data_row_count = max(len(rows) - 1, 0)
    print(f"Number of data rows in the csv file: {data_row_count}")
    print("")
    print_row("Row", "Date", "Amount", "Payee", "Family", "Category")
    print("-" * 120)

    rowNr = 1
    for row in rows[1:]:
        if len(row) < 5:
            print(f"Skipping row {rowNr}: expected 5 columns, got {len(row)} -> {row}")
            rowNr += 1
            continue

        raw_date   = row[0].strip()
        raw_amount = row[1].strip()
        payee      = row[2].strip()
        family     = row[3].strip()
        category   = row[4].strip()

        print_row(rowNr, raw_date, raw_amount, payee, family, category)

        # Parse input date (CSV): DD.MM.YYYY
        try:
            date_obj = datetime.strptime(raw_date, "%d.%m.%Y")
        except ValueError as e:
            print(f"  ! Invalid date in row {rowNr} ('{raw_date}'): {e}. Skipping.")
            rowNr += 1
            continue

        # Format QIF date as DD.MM'YYYY
        qif_date = date_obj.strftime("%d.%m'%Y")

        # Normalize amount
        amount = _normalize_amount(raw_amount)

        # Compose Category for QIF: base category + optional "/Family"
        if family:
            qif_category = f"{category}/{family}"
        else:
            qif_category = category

        # Build QIF transaction in this exact order: D, T, P, L, ^
        qif_data.extend([
            f"D{qif_date}",
            f"T{amount}",
            f"P{payee}",
            f"L{qif_category}",
            "^",
        ])

        rowNr += 1

    try:
        with open(output_file, 'w', encoding='utf-8', newline='') as qif_file:
            qif_file.write('\n'.join(qif_data))
        print("\nQIF file created successfully")
    except OSError as e:
        print(f"Error writing QIF file '{output_file}': {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CSV to QIF (Date;Transaction;Payee;Family members;Category)")
    parser.add_argument('files', nargs='*', default=['input.csv', 'output.qif'], help="Input CSV and optional output QIF path.")
    args = parser.parse_args()

    if len(args.files) == 1:
        csv2qif(input_file=args.files[0])
    else:
        csv2qif(*args.files[:2])
