import click
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

CM_TO_IN = 2.54

GOLDEN_RATIO = 1.618
GOLDEN_RATIO_NARROW = 1.618 - 1

SQRT_TWO = 1.414
SQRT_TWO_NARROW = 1.414 - 1


def convert_cm_to_in(height, width, depth) -> tuple[float, float, float, float]:
    height /= CM_TO_IN
    width /= CM_TO_IN
    depth /= CM_TO_IN
    volume = height * width * depth

    return (height, width, depth, volume)


def find_dimensions(
    start: float,
    end: float,
    lower_bound: float,
    upper_bound: float,
    step: float,
    wide_factor: float,
    narrow_factor: float,
) -> tuple[float, float, float, float]:
    calc_volume_cm3 = 0
    height_cm = start
    width_cm = 0
    depth_cm = 0

    while height_cm < end:
        width_cm = height_cm * wide_factor
        depth_cm = height_cm * narrow_factor
        calc_volume_cm3 = height_cm * width_cm * depth_cm
        logger.debug(
            "%s x %s x %s = %s",
            height_cm,
            width_cm,
            depth_cm,
            calc_volume_cm3,
        )

        if calc_volume_cm3 <= upper_bound and calc_volume_cm3 >= lower_bound:
            break

        height_cm += step

    return (height_cm, width_cm, depth_cm, calc_volume_cm3)


@click.group()
@click.pass_context
@click.option("--start-cm", "-s", type=float, default=20)
@click.option("--end-cm", "-e", type=float, default=40)
@click.option("--step-size", "-x", type=float, default=0.5)
@click.option("--exit-range", "-r", type=float, default=100)
def cli(ctx, start_cm: float, end_cm: float, step_size: float, exit_range: float):
    ctx.obj = {}
    ctx.obj["start"] = start_cm
    ctx.obj["end"] = end_cm
    ctx.obj["step"] = step_size
    ctx.obj["exit_range"] = exit_range


@cli.command()
@click.argument("box_volume_cm3", type=float)
@click.pass_context
def calculate_golden_ratio(ctx, box_volume_cm3: float):
    logger.info(
        "*** Finding parameters for golden ratio box with volume %s cm^3 ***",
        box_volume_cm3,
    )

    upper_bound = box_volume_cm3 + ctx.obj["exit_range"]
    lower_bound = box_volume_cm3 - ctx.obj["exit_range"]

    height_cm, width_cm, depth_cm, calc_volume_cm3 = find_dimensions(
        ctx.obj["start"],
        ctx.obj["end"],
        lower_bound,
        upper_bound,
        ctx.obj["step"],
        GOLDEN_RATIO,
        GOLDEN_RATIO_NARROW,
    )
    logger.info(
        "*** Found size: %s cm x %s cm x %s cm = %s cm^3 ***",
        height_cm,
        width_cm,
        depth_cm,
        calc_volume_cm3,
    )

    height_in, width_in, depth_in, volume_in3 = convert_cm_to_in(
        height_cm, width_cm, depth_cm
    )
    logger.info(
        "*** Found size: %s in x %s in x %s in = %s in^3 ***",
        height_in,
        width_in,
        depth_in,
        volume_in3,
    )


@cli.command()
@click.argument("box_volume_cm3", type=float)
@click.pass_context
def calculate_sqrt_two(ctx, box_volume_cm3: float):
    logger.info(
        "*** Finding parameters for sqrt two box with volume %s cm^3 ***",
        box_volume_cm3,
    )

    upper_bound = box_volume_cm3 + ctx.obj["exit_range"]
    lower_bound = box_volume_cm3 - ctx.obj["exit_range"]

    height_cm, width_cm, depth_cm, calc_volume_cm3 = find_dimensions(
        ctx.obj["start"],
        ctx.obj["end"],
        lower_bound,
        upper_bound,
        ctx.obj["step"],
        SQRT_TWO,
        SQRT_TWO_NARROW,
    )
    logger.info(
        "*** Found size: %s cm x %s cm x %s cm = %s cm^3 ***",
        height_cm,
        width_cm,
        depth_cm,
        calc_volume_cm3,
    )

    height_in, width_in, depth_in, volume_in3 = convert_cm_to_in(
        height_cm, width_cm, depth_cm
    )
    logger.info(
        "*** Found size: %s in x %s in x %s in = %s in^3 ***",
        height_in,
        width_in,
        depth_in,
        volume_in3,
    )


if __name__ == "__main__":
    cli()
