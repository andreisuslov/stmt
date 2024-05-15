import os
import click
import pandas as pd
from datetime import datetime
from hashlib import sha256
from .log import get_logger

logger = get_logger()

# Assuming we have a config setup similar to your detailed functionality
class StatementConfig:
    def __init__(self, bank_name, account_type):
        self.bank_name = bank_name
        self.account_type = account_type

    @staticmethod
    def identify_bank_name(columns):
        """
        Identifies the bank name based on the column headers of the transaction file.
        
        Args:
            columns (list): List of column headers from the transaction file.
            
        Returns:
            str: Identified bank name.
        """
        chase_columns = {'Transaction Date', 'Post Date', 'Description', 'Category', 'Type', 'Amount', 'Memo'}
        boa_columns = {'Posted Date', 'Reference Number', 'Payee', 'Address', 'Amount'}

        if set(columns) == chase_columns:
            return 'Chase'
        elif set(columns) == boa_columns:
            return 'Bank of America'
        else:
            return 'Unknown'

def generate_hash(file_path):
    hash_object = sha256()
    stats = os.stat(file_path)
    metadata = f"{stats.st_ctime}-{stats.st_mtime}"
    hash_object.update(metadata.encode("utf-8"))
    return hash_object.hexdigest()[:6]

def generate_name(input_file, statement_config):
    directory = os.path.dirname(input_file)
    file_timestamp = datetime.fromtimestamp(os.path.getmtime(input_file))
    file_uuid = generate_hash(input_file)
    filename = f"{statement_config.bank_name}-{statement_config.account_type}-{file_timestamp.year}-{file_timestamp.month:02d}-{file_uuid}.csv"
    return os.path.join(directory, filename)

def split_amount(df):
    """
    Splits the Amount column into two columns: Credit and Debit.
    Debit contains negative values and Credit contains positive values.
    """
    df['Credit'] = df['Amount'].apply(lambda x: x if x > 0 else None)
    df['Debit'] = df['Amount'].apply(lambda x: -x if x < 0 else None)
    return df.drop(columns=['Amount'])

def clean_empty_values(df):
    """
    Removes rows where both Credit and Debit are None.
    Also, ensures that zeros do not appear in the Credit and Debit columns.
    """
    # Remove rows where both Credit and Debit are None
    df = df.dropna(subset=['Credit', 'Debit'], how='all')
    # Replace zeros with None for cleaner output
    df['Credit'].replace({0: None}, inplace=True)
    df['Debit'].replace({0: None}, inplace=True)
    return df


def sort_transactions(df):
    """
    Sorts the transactions in ascending order by the "Posted Date" column.
    """
    df['Posted Date'] = pd.to_datetime(df['Posted Date'])
    df = df.sort_values('Posted Date', ascending=True)
    df['Posted Date'] = df['Posted Date'].dt.strftime('%m/%d/%Y')
    return df

def drop_columns(df, columns):
    """
    Drops specified columns from the DataFrame.
    """
    return df.drop(columns=columns, errors='ignore')

@click.command()
@click.argument('input_file')
@click.option('--output_file', '-o', help='Path to the output CSV file', default=None)
def process_statement(input_file, output_file):
    """
    Removes 'Reference Number' and 'Address' columns from a CSV file if they exist.
    Splits 'Amount' into 'Credit' and 'Debit' and cleans up empty values.
    Sorts the transactions in ascending order by the "Posted Date" column.
    Generates an output filename in the same directory as the input file if not specified.
    """
    try:
        df = pd.read_csv(input_file)
        # Identify the bank name based on the column headers
        bank_name = StatementConfig.identify_bank_name(df.columns.tolist())
        # Assume some default config if not provided
        statement_config = StatementConfig(bank_name=bank_name, account_type="credit")
        # Check if the columns exist and drop them if they do
        if statement_config.bank_name == 'Chase':
            columns_to_drop = ['Memo', 'Post Date', 'Type']
            df = drop_columns(df, columns_to_drop)
        if statement_config.bank_name == 'Bank of America':
            columns_to_drop = ['Reference Number', 'Address']
            df = drop_columns(df, columns_to_drop)
        # Split the Amount into Credit and Debit and clean empty values
        df = split_amount(df)
        df = clean_empty_values(df)
        # Sort the transactions in ascending order
        df = sort_transactions(df)
        if not output_file:
            output_file = generate_name(input_file, statement_config)
        df.to_csv(output_file, index=False)
        logger.info(f"File saved to {output_file}")
    except FileNotFoundError as e:
        logger.error(f"File not found: {input_file}")
        click.echo(f"Error: {str(e)}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        click.echo(f"Error: {str(e)}")

if __name__ == '__main__':
    process_statement()
