# Comparison and Alignment of Camera Setups

This programs help to retrieve data to compare data.
Furthermore alignments for cameras with fixed angles can e suggested.

## Usage

### Calculator for fixed solutions

Calculates the areas monitored by x_cameras. The result is either printed to the console or
saved in the file given by the `-o` argument.

```
usage: run_solution.py [-h] [-o OUT] input

SolutionCalculator

positional arguments:
  input              The location of the input json file

optional arguments:
  -h, --help         show this help message and exit
  -o OUT, --out OUT  The location of the calculaed json file. If None output
                     isprinted to the console.
```

Sample usage:

```
python3 run_solution.py example_json/setup1_solution.json
```

### Suggesting camera alignments

Suggests possible camera alignments for cameras with fixed position.
Results are printed to the console or stored in the file given by the `-o` argument.

```
usage: run_suggestion.py [-h] [-o OUT] [-b] input

SolutionCalculator

positional arguments:
  input              The location of the input json file

optional arguments:
  -h, --help         show this help message and exit
  -o OUT, --out OUT  The location of the calculaed json file. If None output
                     isprinted to the console.
  -b, --best         export only the best solutions

```

Sample usage:

```
python3 run_suggestion.py example_json/setup1_solution.json
```

### Example Configs

Example setups can be found in in the folder `example_json`

### Create new json config files

To create new configurations use the `solution_config_generator.py` and
`suggestion_config_generator.py` scrips.
Both have a very simple interface in the command line.
