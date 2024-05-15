import os
import click
import pandas as pd
from datetime import datetime
from hashlib import sha256
from .log import get_logger

logger = get_logger()

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
    df['Credit'] = df['Credit'].replace({0: None})
    df['Debit'] = df['Debit'].replace({0: None})
    return df

def sort_transactions(df, date_column):
    """
    Sorts the transactions in ascending order by the "Posted Date" column.
    """
    df[date_column] = pd.to_datetime(df[date_column])
    df = df.sort_values(date_column, ascending=True)
    df[date_column] = df[date_column].dt.strftime('%m/%d/%Y')
    return df

def drop_columns(df, columns):
    """
    Drops specified columns from the DataFrame.
    """
    return df.drop(columns=columns, errors='ignore')

def rename_column_title(df, old_title, new_title):
    df.rename(columns={old_title: new_title}, inplace=True)
    return df

@click.command()
@click.argument('input_files', nargs=-1, type=click.Path(exists=True))
@click.option('--output_dir', '-o', help='Directory to save the output CSV files', default=None, type=click.Path())
def process_statements(input_files, output_dir):
    for input_file in input_files:
        try:
            df = pd.read_csv(input_file)
            if df is None or df.empty:
                logger.error(f"DataFrame is None or empty after reading {input_file}")
                click.echo(f"Error: DataFrame is None or empty for {input_file}.")
                continue

            logger.info(f"Columns in the input file: {df.columns.tolist()}")

            bank_name = StatementConfig.identify_bank_name(df.columns.tolist())
            if bank_name == 'Unknown':
                logger.error(f"Unknown bank name based on columns: {df.columns.tolist()}")
                click.echo(f"Error: Unknown bank name for {input_file}.")
                continue

            statement_config = StatementConfig(bank_name=bank_name, account_type="credit")

            date_column = None
            if statement_config.bank_name == 'Chase':
                columns_to_drop = ['Memo', 'Post Date', 'Type']
                df = drop_columns(df, columns_to_drop)
                df = rename_column_title(df, 'Transaction Date', 'Date')
            elif statement_config.bank_name == 'Bank of America':
                columns_to_drop = ['Reference Number', 'Address']
                df = drop_columns(df, columns_to_drop)
                df = rename_column_title(df, 'Posted Date', 'Date')
                df = rename_column_title(df, 'Payee', 'Description')

            date_column = 'Date'

            df = split_amount(df)
            if df is None or df.empty:
                logger.error("DataFrame is None or empty after splitting amount.")
                click.echo(f"Error: DataFrame is None or empty after splitting amount for {input_file}.")
                continue

            df = clean_empty_values(df)
            if df is None or df.empty:
                logger.error("DataFrame is None or empty after cleaning empty values.")
                click.echo(f"Error: DataFrame is None or empty after cleaning empty values for {input_file}.")
                continue

            df = sort_transactions(df, date_column)
            if df is None or df.empty:
                logger.error("DataFrame is None or empty after sorting transactions.")
                click.echo(f"Error: DataFrame is None or empty after sorting transactions for {input_file}.")
                continue

            if not output_dir:
                output_file = generate_name(input_file, statement_config)
            else:
                output_file = os.path.join(output_dir, os.path.basename(generate_name(input_file, statement_config)))

            df.to_csv(output_file, index=False)
            logger.info(f"File saved to {output_file}")
            click.echo(f"File saved to {output_file}")

        except FileNotFoundError as e:
            logger.error(f"File not found: {input_file}")
            click.echo(f"Error: {str(e)}")
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            click.echo(f"Error: {str(e)}")

if __name__ == '__main__':
    process_statements()
