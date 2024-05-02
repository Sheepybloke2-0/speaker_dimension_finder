import click
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

GOLDEN_RATIO = 1.618
GOLDEN_RATIO_NARROW = 1.618 - 1


@click.group()
def cli():
    pass


@cli.command()
@click.option("--start-cm", "-s", type=float, default=20)
@click.option("--end-cm", "-e", type=float, default=40)
@click.option("--step-size", "-x", type=float, default=0.5)
@click.option("--exit-range", "-r", type=float, default=100)
@click.argument("box_volume_cm3", type=float)
def calculate_golden_ratio_box(
    box_volume_cm3: float, start_cm: float, end_cm: float, step_size: float, exit_range: float
):
    logger.info("*** Finding parameters for box with volume %s cm^3 ***", box_volume_cm3)
    calc_volume_cm3 = 0
    height_cm = start_cm
    width_cm = 0
    depth_cm = 0

    while height_cm < end_cm:
        width_cm = height_cm * GOLDEN_RATIO
        depth_cm = height_cm * GOLDEN_RATIO_NARROW
        calc_volume_cm3 = height_cm * width_cm * depth_cm
        logger.info(
            "%s x %s x %s = %s",
            height_cm,
            width_cm,
            depth_cm,
            calc_volume_cm3,
        )

        if (
            calc_volume_cm3 <= box_volume_cm3 + exit_range
            and calc_volume_cm3 >= box_volume_cm3 - exit_range
        ):
            logger.info(
                "*** Found size: %s x %s x %s = %s ***",
                height_cm,
                width_cm,
                depth_cm,
                calc_volume_cm3,
            )
            break

        height_cm += step_size

if __name__ == "__main__":
    cli()
