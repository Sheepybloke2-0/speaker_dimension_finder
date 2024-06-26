import logging
import math

import click

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

CM_TO_IN = 2.54

GOLDEN_RATIO = 1.618
GOLDEN_RATIO_NARROW = 1.618 - 1

SQRT_TWO = 1.414
SQRT_TWO_NARROW = 1.414 - 1


def convert_cm_to_in(value: float) -> float:
    return value / CM_TO_IN


def convert_cm_to_in_rect(height, width, depth) -> tuple[float, float, float, float]:
    height = convert_cm_to_in(height)
    width = convert_cm_to_in(width)
    depth = convert_cm_to_in(depth)
    volume = height * width * depth

    return (height, width, depth, volume)


def convert_cm_to_in_spheroid(a, b, c) -> tuple[float, float, float, float]:
    a = convert_cm_to_in(a)
    b = convert_cm_to_in(b)
    c = convert_cm_to_in(c)
    volume = math.pi * (4 / 3) * a * b * c

    return (a, b, c, volume)


def find_rectangle_dimensions(
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


def find_sphere_dimensions(
    start: float,
    end: float,
    lower_bound: float,
    upper_bound: float,
    step: float,
) -> tuple[float, float]:
    calc_volume_cm3 = 0
    radius_cm = start

    while radius_cm < end:
        calc_volume_cm3 = math.pi * (4 / 3) * (radius_cm**3)
        logger.debug("%s cm = %s cm^3", radius_cm, calc_volume_cm3)

        if calc_volume_cm3 <= upper_bound and calc_volume_cm3 >= lower_bound:
            break

        radius_cm += step

    return (radius_cm, calc_volume_cm3)


def find_oblate_spheroid_dimensions(
    start: float,
    end: float,
    lower_bound: float,
    upper_bound: float,
    step: float,
    factor: float,
) -> tuple[float, float, float, float]:
    calc_volume_cm3 = 0
    a_radius_cm = start
    b_radius_cm = 0
    c_radius_cm = 0

    while a_radius_cm < end:
        b_radius_cm = a_radius_cm
        # Assume that the B radius = C radius
        c_radius_cm = a_radius_cm * factor

        calc_volume_cm3 = math.pi * (4 / 3) * a_radius_cm * b_radius_cm * c_radius_cm

        if calc_volume_cm3 <= upper_bound and calc_volume_cm3 >= lower_bound:
            break

        a_radius_cm += step

    return (a_radius_cm, b_radius_cm, c_radius_cm, calc_volume_cm3)


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

    height_cm, width_cm, depth_cm, calc_volume_cm3 = find_rectangle_dimensions(
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

    height_in, width_in, depth_in, volume_in3 = convert_cm_to_in_rect(
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

    height_cm, width_cm, depth_cm, calc_volume_cm3 = find_rectangle_dimensions(
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

    height_in, width_in, depth_in, volume_in3 = convert_cm_to_in_rect(
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
@click.argument("sphere_volume_cm3", type=float)
@click.pass_context
def calculate_sphere(ctx, sphere_volume_cm3: float):
    logger.info(
        "*** Finding parameters for ellipsoid with volume %s cm^3 ***",
        sphere_volume_cm3,
    )

    upper_bound = sphere_volume_cm3 + ctx.obj["exit_range"]
    lower_bound = sphere_volume_cm3 - ctx.obj["exit_range"]

    radius_cm, volume_cm3 = find_sphere_dimensions(
        ctx.obj["start"], ctx.obj["end"], lower_bound, upper_bound, ctx.obj["step"]
    )
    logger.info(
        "*** Found size: %s cm = %s cm^3 ***",
        radius_cm,
        volume_cm3,
    )

    radius_in = convert_cm_to_in(radius_cm)
    volume_in3 = math.pi * (4 / 3) * (radius_in**3)
    logger.info(
        "*** Found size: %s in = %s in^3 ***",
        radius_in,
        volume_in3,
    )


@cli.command()
@click.argument("spheroid_volume_cm3", type=float)
@click.option(
    "--factor",
    "-f",
    type=click.Choice(["SQRT", "GOLDEN"], case_sensitive=False),
    default="GOLDEN",
)
@click.option(
    "--narrow",
    "-n",
    is_flag=True,
)
@click.pass_context
def calculate_oblate_spheroid(
    ctx, spheroid_volume_cm3: float, factor: str, narrow: bool
):
    logger.info(
        "*** Finding parameters for oblate spheroid with volume %s cm^3 and %s factor***",
        spheroid_volume_cm3,
        factor,
    )

    upper_bound = spheroid_volume_cm3 + ctx.obj["exit_range"]
    lower_bound = spheroid_volume_cm3 - ctx.obj["exit_range"]
    if narrow:
        factor_value = SQRT_TWO_NARROW if factor == "SQRT" else GOLDEN_RATIO_NARROW
    else:
        factor_value = SQRT_TWO if factor == "SQRT" else GOLDEN_RATIO

    a_radius_cm, b_radius_cm, c_radius_cm, volume_cm3 = find_oblate_spheroid_dimensions(
        ctx.obj["start"],
        ctx.obj["end"],
        lower_bound,
        upper_bound,
        ctx.obj["step"],
        factor_value,
    )

    logger.info(
        "*** Found size: %s cm x %s cm x %s cm = %s cm^3 ***",
        a_radius_cm,
        b_radius_cm,
        c_radius_cm,
        volume_cm3,
    )

    a_radius_in, b_radius_in, c_radius_in, volume_in3 = convert_cm_to_in_spheroid(
        a_radius_cm, b_radius_cm, c_radius_cm
    )
    logger.info(
        "*** Found size: %s in x %s in x %s in = %s in^3 ***",
        a_radius_in,
        b_radius_in,
        c_radius_in,
        volume_in3,
    )


if __name__ == "__main__":
    cli()
