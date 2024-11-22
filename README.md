
# Statement Processor (stmt)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

The Statement Processor (`stmt`) is a command-line tool that processes Bank of America and Chase transaction CSV files and reformats them into a specific format suitable for use in a Google Sheets-based Budget App. This tool simplifies the process of converting the raw transaction data from these banks into a clean and structured format, making it easier to import and analyze the data in your Budget App.

## Features

- Identifies the bank name based on the column headers of the transaction file
- Removes unnecessary columns such as "Reference Number" and "Address" (Bank of America) or "Memo", "Post Date", and "Type" (Chase)
- Splits the "Amount" column into separate "Credit" and "Debit" columns
- Cleans up empty values and ensures that zeros do not appear in the "Credit" and "Debit" columns
- Sorts the transactions in ascending order based on the "Date" column
- Generates an output CSV file with the processed data in the desired format
- Option to unite multiple transaction sheets into one after processing

## Prerequisites

Before installing and using the Statement Processor, ensure that you have the following:

- **Python 3.8 or higher** installed on your system. You can check your Python version with:
  ```bash
  python3 --version
  ```
- [**Poetry**](https://python-poetry.org/) package manager installed. You can install it using:
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```
- [**pipx**](https://pypa.github.io/pipx/) installed for managing Python CLI tools. You can install it using:
  ```bash
  python3 -m pip install --user pipx
  python3 -m pipx ensurepath
  ```

## Installation

To install the Statement Processor, follow these steps:

1. **Clone the Repository**:

   Clone the `stmt` repository from GitHub and navigate to the project directory:
   ```bash
   git clone https://github.com/andreisuslov/stmt.git
   cd stmt
   ```

2. **Install Dependencies and the Command-Line Tool**:

   Use the provided `Makefile` to install the dependencies and the `stmt` command-line tool:
   ```bash
   make install
   ```

   This command will:
   - Check if `pipx` is installed.
   - Configure the project environment using Poetry.
   - Install the `stmt` command-line tool into the default pipx-managed directory (typically `~/.local/bin`).

3. **Add `stmt` to the PATH**:

   If `stmt` is not immediately recognized as a command, ensure that the pipx binary directory (`~/.local/bin`) is included in your system's PATH.

   Add the following line to your shell configuration file (e.g., `~/.zshrc` or `~/.bashrc`):
   ```bash
   export PATH=$HOME/.local/bin:$PATH
   ```

   Reload the shell configuration:
   ```bash
   source ~/.zshrc  # Or ~/.bashrc for bash users
   ```

4. **Verify the Installation**:

   After installation, verify that the `stmt` command is available by running:
   ```bash
   stmt --help
   ```

   If the installation was successful, you will see the help message for the `stmt` command-line tool.


## Usage

Once the installation is complete, you can use the `stmt` command to process your Bank of America or Chase transaction CSV files:

```bash
stmt /path/to/your/transactions.csv
```

Replace `/path/to/your/transactions.csv` with the actual path to your Bank of America or Chase transaction CSV file.

To unite multiple transaction sheets into one, use the `--unite` option:

```bash
stmt --unite /path/to/your/transactions1.csv /path/to/your/transactions2.csv
```

The processed transactions will be saved in a new CSV file located in the same directory as the input file(s). The output file will have a generated name based on the bank name, account type, timestamp, and a unique identifier.

## Uninstallation

To uninstall the Statement Processor, run the following command:

```bash
pipx uninstall stmt
```

## Contributing

Contributions to the Statement Processor are welcome!
