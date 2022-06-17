import sys
import click

from counter import config


@click.group()
def cli():
    pass


@cli.command()
@click.option('-i', "--img-path", required=True, help="The path to the image to be processed")
@click.option('-t', "--threshold", type=float, default=0.9, help="The lower limit for the object detection")
def count(img_path: str, threshold: float):
    with open(img_path, "rb") as img:
        predictions = config.get_count_action().execute(img, threshold)
        print(predictions)


@cli.command()
@click.option('-i', "--img-path", required=True, help="The path to the image to be processed")
@click.option('-t', "--threshold", type=float, default=0.9, help="The lower limit for the object detection")
def predict(img_path: str, threshold: float):
    with open(img_path, "rb") as img:
        predictions = config.get_prediction_action().execute(img, threshold)
        print(predictions)


if __name__ == "__main__":
    cli()
