import click
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

GOLDEN_RATIO = 1.618
GOLDEN_RATIO_NARROW = 1.618 - 1


@click.group()
@click.pass_context
@click.option("--start-cm", "-s", type=float, default=20)
@click.option("--end-cm", "-e", type=float, default=40)
@click.option("--step-size", "-x", type=float, default=0.5)
@click.option("--exit-range", "-r", type=float, default=100)
def cli(
    ctx, start_cm: float, end_cm: float, step_size: float, exit_range: float
):
    ctx.obj = {}
    ctx.obj["start"] = start_cm
    ctx.obj["end"] = end_cm
    ctx.obj["step"] = step_size
    ctx.obj["exit_range"] = exit_range


@cli.command()
@click.argument("box_volume_cm3", type=float)
@click.pass_context
def calculate_golden_ratio(ctx, box_volume_cm3: float):
    logger.info("*** Finding parameters for box with volume %s cm^3 ***", box_volume_cm3)
    calc_volume_cm3 = 0
    height_cm = ctx.obj["start"]
    width_cm = 0
    depth_cm = 0

    upper_bound = box_volume_cm3 + ctx.obj["exit_range"]
    lower_bound = box_volume_cm3 - ctx.obj["exit_range"]

    while height_cm < ctx.obj["end"]:
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
            calc_volume_cm3 <= upper_bound
            and calc_volume_cm3 >= lower_bound
        ):
            logger.info(
                "*** Found size: %s x %s x %s = %s ***",
                height_cm,
                width_cm,
                depth_cm,
                calc_volume_cm3,
            )
            break

        height_cm += ctx.obj["step"]

if __name__ == "__main__":
    cli()
