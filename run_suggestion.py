import argparse
import logging
import json

from app.suggestor import Suggestor, ExportSuggestor


log = logging.getLogger(__name__)


def check_json(json_file):
    keys = ['cameras', 'max_distance', 'angle_of_view', 'field_len_x', 'field_len_y', 'field_origin_x',
            'field_origin_y']
    message = "The key %s is not in the json config file"
    for key in keys:
        if key not in json_file:
            raise KeyError(message % key)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="SolutionCalculator")
    parser.add_argument('input',help='The location of the input json file')
    parser.add_argument('-o', '--out', help='The location of the calculaed json file. If None output is'
                                            'printed to the console.', default=None)
    parser.add_argument('-b', '--best', help="export only the best solutions", action="store_true")

    args = parser.parse_args()

    logconf = {'format': '[%(asctime)s.%(msecs)-3d: %(name)-16s - %(levelname)-5s] %(message)s', 'datefmt': "%H:%M:%S"}

    logging.basicConfig(level=logging.INFO, **logconf)

    with open(args.input) as f:
        config = json.load(f)

    sug = Suggestor(config['cameras'], float(config['max_distance']), float(config['angle_of_view']),
                    float(config['field_len_x']), float(config['field_len_y']),
                    float(config['field_origin_x']), float(config['field_origin_y']))
    sug.run()

    if args.out is None:
        if args.best is True:
            d = ExportSuggestor.create_best_dict(sug)
            print(json.dumps(d, indent=4, sort_keys=True))
        else:
            d = ExportSuggestor.create_dict(sug)
            print(json.dumps(d, indent=4, sort_keys=True))
    else:
        if args.best is True:
            d = ExportSuggestor.write_best_to_file(sug, args.out)
        else:
            d = ExportSuggestor.write_best_to_file(sug, args.out)
