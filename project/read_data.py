import sys
import click
import os
import pandas as pd
from sklearn.datasets import load_iris


@click.group()
def main():
    print("read_data main")


@main.command()
@click.option('--output-path', type=click.Path(exists=False, file_okay=False), default='project')
def read_data(output_path):
    print("read_data")
    os.makedirs(output_path, exist_ok=True)
    iris = load_iris()
    data = pd.DataFrame(iris.data)
    data.to_csv(f'{output_path}/iris.csv')


if __name__ == '__main__':
    sys.exit(main())
