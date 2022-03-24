import json
from textx import metamodel_for_language
from kerml.classes.root_layer import Element, NonFeatureElement, Relationship, Annotation, ModelComment, \
    TextualRepresentation, AliasMember, FeatureNamespaceMember, NonFeatureMember, Import, OwnedDocumentation, Namespace
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
    from kernel_layer import Package
    entity_mm = metamodel_from_file(join(current_dir, 'root', 'root.tx'),
                                    classes=[Element, NonFeatureElement, Relationship, Annotation, ModelComment,
                                             OwnedDocumentation, Namespace, TextualRepresentation,
                                             Import, NonFeatureMember, FeatureNamespaceMember, AliasMember],
                                    use_regexp_group=True,
                                    autokwd=True,
                                    debug=debug)
    return entity_mm


class KermlFiles(object):
    def __init__(self):
        self.kerml_files = {}

    def get_test_file(self, kerml_file_name, namespace=None):
        # TODO: This can be cleaned up but I'm lazy
        tpath = ""

        if f"{namespace}.{kerml_file_name}" in self.kerml_files.keys():
            tpath = self.kerml_files[f"{namespace}.{kerml_file_name}"]
        else:
            for k in self.kerml_files.keys():
                s = k.split(kerml_file_name)
                if len(s) > 1:
                    tpath = self.kerml_files[f"{s[0]}{kerml_file_name}"]
        return join(tpath, kerml_file_name)

    def add_file(self, qfn, file_path):
        self.kerml_files[qfn] = file_path

    def __str__(self):
        return json.dumps(self.kerml_files, indent=2, separators=(',', ':'))


def load_examples(kerml_dirs: list):
    kerml_files = KermlFiles()

    for kd in kerml_dirs:
        for w in os.walk(kd):
            for f in w[2]:
                if '.kerml' in f:
                    qualified_name = w[0].replace(' ', '_').split('/')[-1] + "." + f
                    kerml_files.add_file(qualified_name, w[0])
    return kerml_files


def main(test_file, debug=False):
    element_mm = get_element_mm(debug)
    # element_mm.register_scope_providers({
    #     "Element.*": root_layer.relationship_definer_scope,
    #     "Relationship.*": root_layer.relationship_definer_scope,
    #     "RelationshipOwnedElement.*": root_layer.relationship_definer_scope,
    # })
    model = element_mm.model_from_file(test_file)
    model_export(model, join(current_dir, '../_dot_files', 'root_mm.dot'))


def inspect_language(grammar_file):
    textx_mm = metamodel_for_language("textx")
    grammar_model = textx_mm.grammar_model_from_file(join(current_dir, grammar_file))
    print(grammar_model)


if __name__ == "__main__":
    test_files = load_examples(["/Users/dank/git/systems-modeling/SysML-v2-Release",
                                "/Users/dank/git/systems-modeling/SysML-v2-Grammar-Parser/kerml/root/test"])

    # print(f"Testing {test_files}")
    tfile = test_files.get_test_file("ElementDocRelationship.kerml", "test")
    print(f"Testing {tfile}")
    main(tfile, debug=True)
