# Credit Card Checker

A beautiful CLI tool to validate credit card numbers using Luhn's algorithm and display detailed card information.

## Features

- Validates credit card numbers using Luhn's algorithm
- Identifies card type (Visa, MasterCard, American Express, Discover)
- Validates expiration date
- Validates CVV
- Beautiful CLI interface with colored output
- Supports two input formats:
  - `number|mm/yy|cvv`
  - `number|mm|yy|cvv`

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the program:
```bash
python cc_checker.py
```

Enter card details in either format:
- `number|mm/yy|cvv` (e.g., `4532015112830366|12/25|123`)
- `number|mm|yy|cvv` (e.g., `4532015112830366|12|25|123`)

Type `exit` to quit the program.

## Example Output

The program will display:
- Card number validation (Luhn's algorithm)
- Card type
- Expiration date validation
- CVV validation
- Final result (VALID/INVALID) 