import json

from kerml.model_processing import owned_specialization_definer_scope
from textx import metamodel_for_language
from kerml.classes.root_layer import Element, NonFeatureElement, Relationship, Annotation, \
    ModelComment, \
    TextualRepresentation, AliasMember, FeatureNamespaceMember, NonFeatureMember, Import, \
    OwnedDocumentation, Namespace, \
    Membership
from kerml.classes.core_layer import Type, FeatureElement, Specialization, Conjugation, Disjoining, \
    TypeFeaturing, \
    FeatureMember, Feature, Multiplicity, Classifier, Subclassification, Subsetting, Redefinition, \
    FeatureTyping, FeatureChaining, EndFeatureMembership
from kerml.classes.kernel_layer import Class, DataType, Structure, Association, \
    AssociationStructure, Connector, BindingConnector, Succession, Behavior, Step, \
    ParameterMembership, Function, Predicate, Expression, BooleanExpression, Invariant, \
    ReturnParameterMembership, ResultExpressionMembership, LiteralExpression, LiteralInteger, \
    NullExpression, SelectExpression, MultiplicityRange, MetadataFeatureValue, \
    FeatureReferenceExpression, InvocationExpression, LiteralBoolean, LiteralString, \
    LiteralInfinity, CollectExpression, FeatureValue, SuccessionItemFlow, FeatureChainExpression, \
    OperatorExpression, LiteralRational, Interaction, ItemFlow, AnnotatingFeature, MetadataFeature, \
    Package, ElementFilterMembership
from textx.export import model_export
from textx import language, metamodel_from_file
from os.path import join
import os

__version__ = "0.1.0.dev"

current_dir = os.path.dirname(__file__)


def class_provider(name):
    classes = [
        AliasMember, Annotation, Element,
        FeatureNamespaceMember, Import,
        ModelComment, Membership, Namespace, NonFeatureElement,
        NonFeatureMember, OwnedDocumentation, Relationship, TextualRepresentation,

        Type, FeatureElement, TypeFeaturing, FeatureMember, Specialization,
        Conjugation, Disjoining, Feature, Multiplicity, Classifier, Subclassification, Subsetting,
        Redefinition, FeatureTyping, FeatureChaining, EndFeatureMembership,

        Class, DataType, Structure, Association, AssociationStructure, Connector, BindingConnector,
        Succession, Behavior, Step, ParameterMembership, Function, Predicate, Expression,
        BooleanExpression, Invariant, ReturnParameterMembership, ResultExpressionMembership,
        FeatureReferenceExpression, InvocationExpression, LiteralExpression, LiteralInteger,
        LiteralRational, LiteralBoolean, LiteralString, LiteralInfinity, NullExpression,
        OperatorExpression, FeatureChainExpression, CollectExpression, SelectExpression,
        Interaction, ItemFlow, SuccessionItemFlow, FeatureValue, MultiplicityRange,
        AnnotatingFeature, MetadataFeature, MetadataFeatureValue, Package, ElementFilterMembership
    ]
    classes = dict(map(lambda x: (x.__name__, x), classes))
    return classes.get(name)


@language('kerml', '*.kerml')
def kerml_language():
    """KerML - Kernel Modeling Language"""
    mm = metamodel_from_file(join(current_dir, 'kerml.tx'),
                             classes=class_provider,
                             use_regexp_group=True,
                             autokwd=True,
                             debug=False,
                             auto_init_attributes=False)

    # Here if necessary register object processors or scope providers
    # http://textx.github.io/textX/stable/metamodel/#object-processors
    # http://textx.github.io/textX/stable/scoping/
    mm.register_scope_providers({'OwnedSpecialization.*': owned_specialization_definer_scope})

    return mm


def get_element_mm(debug=False):
    """
    Builds and returns a meta-model for Entity language.
    """
    from kernel_layer import Package
    entity_mm = metamodel_from_file(join(current_dir, 'kerml.tx'),
                                    classes=class_provider,
                                    use_regexp_group=True,
                                    autokwd=True,
                                    debug=debug,
                                    auto_init_attributes=False)
    entity_mm.register_scope_providers({'OwnedSpecialization.*': owned_specialization_definer_scope})
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
    model_export(model, join(current_dir, '../_dot_files', 'kerml_mm.dot'))


def inspect_language(grammar_file):
    textx_mm = metamodel_for_language("textx")
    grammar_model = textx_mm.grammar_model_from_file(join(current_dir, grammar_file))
    print(grammar_model)


if __name__ == "__main__":
    test_files = load_examples(["/Users/dank/git/systems-modeling/SysML-v2-Release",
                                "/Users/dank/git/systems-modeling/SysML-v2-Grammar-Parser/kerml/test"])

    # inspect_language("./root/kerml.tx")
    # print(f"Testing {test_files}")
    tests = [
        "ElementDocRelationship.kerml",
        "baseline.kerml",
        "elements.kerml",
        # "features.kerml",
        "simple_features.kerml",
        "simpletypes.kerml",
        "typeconjugation.kerml"
    ]
    for test in tests:
        tfile = test_files.get_test_file(test, "test")
        print(f"Testing {tfile}")
        main(tfile, debug=False)
        print(f"PASSED: {test}")

    print("==========")
    print("TESTING Model Library: Base.kerml")
    base_kerml = "/Users/dank/git/systems-modeling/SysML-v2-Release/sysml.library/Kernel Library/Base.kerml"
    main(base_kerml)
    print("==========")
