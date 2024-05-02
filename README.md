# Speaker Box Dimension Finder

Calculates the dimensions of a speaker based on a specified volume in cm^3.

Currently supports using the golden ratio and the square root of 2.

```shell
❯ python dimension_finder.py --help
Usage: dimension_finder.py [OPTIONS] COMMAND [ARGS]...

Options:
  -s, --start-cm FLOAT
  -e, --end-cm FLOAT
  -x, --step-size FLOAT
  -r, --exit-range FLOAT
  --help                  Show this message and exit.

Commands:
  calculate-golden-ratio
```

Example:
```shell
python dimension_finder.py -r 250 -x 0.1  calculate-golden-ratio 25000
```

Starts the search at 20cm for the height, and steps by 0.1 cm until the calculated volume is within +/- 250 cm^3 of the specified volume, 25,000.


