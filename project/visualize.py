import sys
import click
import os
import pandas as pd
import matplotlib.pyplot as plt
from azureml.core.run import Run


@click.group()
def main():
    print("visualize main")


@main.command()
@click.option('--input-path', type=click.Path(exists=False, file_okay=False), default='project')
@click.option('--chart', type=str, default='line')
def visualize(input_path, chart):
    print("visualize")
    run = Run.get_context()
    data = pd.read_csv(f"{input_path}/iris_processed.csv", index_col=0)
    print(data.head)

    if chart == "line":
        fig, ax = plt.subplots()
        ax.plot(data.SepalLengthCm)
        ax.plot(data.SepalWidthCm)
        ax.plot(data.PetalLengthCm)
        ax.plot(data.PetalWidthCm)
        run.log_image(f"line_plot", plot=plt)
    elif chart == "hist":
        fig, ax = plt.subplots()
        ax.hist(data.SepalLengthCm)
        ax.hist(data.SepalWidthCm)
        ax.hist(data.PetalLengthCm)
        ax.hist(data.PetalWidthCm)
        run.log_image(f"hist_plot", plot=plt)
    elif chart == "scatter":
        fig, ax = plt.subplots()
        ax.scatter(data.index, data.SepalLengthCm)
        ax.scatter(data.index, data.SepalWidthCm)
        ax.scatter(data.index, data.PetalLengthCm)
        ax.scatter(data.index, data.PetalWidthCm)
        run.log_image(f"scatter_plot", plot=plt)
    else: # By default, we use Line plot
        fig, ax = plt.subplots()
        ax.plot(data.SepalLengthCm)
        ax.plot(data.SepalWidthCm)
        ax.plot(data.PetalLengthCm)
        ax.plot(data.PetalWidthCm)
        run.log_image(f"line_plot", plot=plt)


if __name__ == '__main__':
    sys.exit(main())
