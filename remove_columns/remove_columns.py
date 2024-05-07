import os
import click
import pandas as pd
from datetime import datetime
from hashlib import sha256

# Assuming we have a config setup similar to your detailed functionality
class StatementConfig:
    def __init__(self, bank_name, account_type):
        self.bank_name = bank_name
        self.account_type = account_type

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

@click.command()
@click.argument('input_file')
@click.option('--output_file', '-o', help='Path to the output CSV file', default=None)
def remove_columns(input_file, output_file):
    """
    Removes 'Reference Number' and 'Address' columns from a CSV file if they exist.
    Splits 'Amount' into 'Credit' and 'Debit' and cleans up empty values.
    Generates an output filename in the same directory as the input file if not specified.
    """
    df = pd.read_csv(input_file)

    # Check if the columns exist and drop them if they do
    columns_to_drop = ['Reference Number', 'Address']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')

    # Split the Amount into Credit and Debit and clean empty values
    df = split_amount(df)
    df = clean_empty_values(df)

    if not output_file:
        # Assume some default config if not provided
        statement_config = StatementConfig(bank_name="defaultbank", account_type="credit")
        output_file = generate_name(input_file, statement_config)

    df.to_csv(output_file, index=False)
    click.echo(f"File saved to {output_file}")

if __name__ == '__main__':
    remove_columns()
