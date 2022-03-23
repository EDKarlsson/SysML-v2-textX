import argparse
import os

__version__ = "0.1.0.dev"

current_dir = os.path.dirname(__file__)

FUNCTION_MAP = {
    # 'kerml': kerml.kerml_language,
    'root': print,
}

if __name__ == "__main__":
    """
    This is mainly for testing during development.
    """
    parser = argparse.ArgumentParser(description='KerML TextX Model CLI')
    parser.add_argument('layer', type=str,
                        help='Select Metamodel Layer of the Kernel Modeling Language to run textX on')
    parser.add_argument('--debug', type=bool, default=True, help='Enable debug output')
    args = parser.parse_args()
    func = FUNCTION_MAP[args.layer]
    func(args.debug)
