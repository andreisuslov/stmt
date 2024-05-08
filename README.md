# Statement Processor (stmt)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

The Statement Processor (`stmt`) is a command-line tool that processes Bank of America transaction CSV files and reformats them into a specific format suitable for use in a Google Sheets-based Budget App. This tool simplifies the process of converting the raw transaction data from Bank of America into a clean and structured format, making it easier to import and analyze the data in your Budget App.

## Features

- Removes unnecessary columns such as "Reference Number" and "Address" from the input CSV file
- Splits the "Amount" column into separate "Credit" and "Debit" columns
- Cleans up empty values and ensures that zeros do not appear in the "Credit" and "Debit" columns
- Sorts the transactions in ascending order based on the "Posted Date" column
- Generates an output CSV file with the processed data in the desired format

## Prerequisites

Before installing and using the Statement Processor, ensure that you have the following:

- Python 3.x installed on your system
- [Poetry](https://python-poetry.org/) package manager installed

## Installation

To install the Statement Processor, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/andreisuslov/stmt.git
   cd stmt
   ```

2. Install the dependencies and the command-line tool using the provided Makefile:

   ```bash
   make install
   ```

   This command will check if `pipx` is installed, configure the project using Poetry, and install the `stmt` command-line tool.

## Usage

Once the installation is complete, you can use the `stmt` command to process your Bank of America transaction CSV files:

```bash
stmt /path/to/your/transactions.csv
```

Replace `/path/to/your/transactions.csv` with the actual path to your Bank of America transaction CSV file.

The processed transactions will be saved in a new CSV file located in the same directory as the input file. The output file will have a generated name based on the bank name, account type, timestamp, and a unique identifier.

## Uninstallation

To uninstall the Statement Processor, run the following command:

```bash
pipx uninstall stmt
```

## Contributing

Contributions to the Statement Processor are welcome!
