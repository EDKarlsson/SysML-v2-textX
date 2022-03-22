from os.path import exists, dirname, join
from textx import metamodel_from_file
from textx.export import model_export
from classes import root

this_folder = dirname(__file__)


def get_element_mm():
    """
    Builds and returns a meta-model for Entity language.
    """
    entity_mm = metamodel_from_file(join(this_folder, 'elements.tx'),
                                    classes=[root.Element, root.Relationship],
                                    debug=True)

    return entity_mm


def main():
    root_elements = "./elements/test/elements.kerml"
    element_mm = get_element_mm()
    model = element_mm.model_from_file(root_elements)
    model_export(model, join(this_folder,'dot_files', 'elements_mm.dot'))


if __name__ == "__main__":
    main()
