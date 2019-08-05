import sys
import click
import os
import pandas as pd


@click.group()
def main():
    print("pre_process main")


@main.command()
@click.option('--input-path', type=click.Path(exists=False, file_okay=False), default='project')
@click.option('--output-path', type=click.Path(exists=False, file_okay=False), default='project')
def pre_process(input_path, output_path):
    print("pre_process")
    os.makedirs(output_path, exist_ok=True)
    data = pd.read_csv(f"{input_path}/iris.csv", index_col=0)
    data.rename(columns={"0": "SepalLengthCm", "1": "SepalWidthCm", "2": "PetalLengthCm", "3": "PetalWidthCm"}, inplace=True)
    data.ffill()
    data.to_csv(f'{output_path}/iris_processed.csv')


if __name__ == '__main__':
    sys.exit(main())
