from textx import language, metamodel_from_file
import argparse
import os

import root

__version__ = "0.1.0.dev"

current_dir = os.path.dirname(__file__)


@language('kerml', '*.kerml')
def kerml_language():
    """KerML - Kernel Modeling Language"""
    mm = metamodel_from_file(os.path.join(current_dir, 'kerml.tx'))

    # Here if necessary register object processors or scope providers
    # http://textx.github.io/textX/stable/metamodel/#object-processors
    # http://textx.github.io/textX/stable/scoping/

    return mm


def root_mm():
    root.main()


FUNCTION_CALLS = {
    'root': root_mm,
    'kerml': kerml_language
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='KerML TextX Model CLI')
    parser.add_argument('layer', metavar='L', type=str, nargs='+',
                        help='Select Metamodel Layer of the Kernel Modeling Language to run textX on')
    args = parser.parse_args()
