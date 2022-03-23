from kerml.classes.root_layer import *
from textx.export import model_export
from textx import language, metamodel_from_file
from os.path import join
import os

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


def get_element_mm(debug=False):
    """
    Builds and returns a meta-model for Entity language.
    """
    entity_mm = metamodel_from_file(join(current_dir, 'root', 'root.tx'),
                                    classes=[Element, Relationship,
                                             Annotation, ModelComment, OwnedDocumentation],
                                    use_regexp_group=True,
                                    autokwd=True,
                                    debug=debug)
    return entity_mm


def main(debug=False):
    element_mm = get_element_mm(debug)
    kerml_test_file = "./root/test/elements.kerml"
    # kerml_test_file = "../../SysML-v2-Release/kerml/src/examples/Simple Tests/Elements.kerml"
    model = element_mm.model_from_file(join(current_dir, kerml_test_file))
    model_export(model, join(current_dir, '../_dot_files', 'root_mm.dot'))


if __name__ == "__main__":
    main()
