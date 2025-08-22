# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple Python utility that converts CSV files to QIF (Quicken Interchange Format) files. The project consists of a single main script (`csv2qif.py`) with no external dependencies beyond Python's standard library.

## Core Architecture

The application is structured around a single main function `csv2qif()` in `csv2qif.py` that:
- Reads semicolon-delimited CSV files with UTF-8-BOM encoding
- Processes transactions with 5 columns: Date, Amount, Payee, Family, Category
- Outputs QIF format with specific field ordering: Date, Transaction, Payee, Category, End marker

### Key Implementation Details

- **Date handling**: Input expects `DD.MM.YYYY` format, outputs QIF format `DD.MM'YYYY`
- **Amount normalization**: `_normalize_amount()` function handles various decimal/thousands separators
- **Category composition**: Combines base category with optional family member as `Category/Family`
- **Error handling**: Gracefully skips malformed rows and provides detailed console output

## Running the Application

```bash
# Basic usage with default files (input.csv -> output.qif)
python csv2qif.py

# Specify input file only (outputs to output.qif)
python csv2qif.py input_file.csv

# Specify both input and output files
python csv2qif.py input_file.csv output_file.qif
```

## CSV Format Requirements

The CSV must be semicolon-delimited with exactly 5 columns:
1. Date (DD.MM.YYYY format)
2. Amount (signed decimal, negative for expenses)
3. Payee (transaction party name)
4. Family (optional family member, can be empty)
5. Category (transaction category)

Note: The sample CSV files in the repository use an older 4-column format (Date;Amount;Payee;Memo) which doesn't match the current code implementation that expects 5 columns.

## Testing

Test the application by running it against the sample files:
```bash
python csv2qif.py input.csv test_output.qif
```

The application provides verbose console output showing each processed row, making it easy to verify correct parsing and conversion.