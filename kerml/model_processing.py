from pprint import pprint

import kerml
from textx.scoping import providers, Postponed
from textx import get_model, get_metamodel, get_location, get_children, get_children_of_type


def print_model_elem(model, elem, attr, attr_ref):
    print(f'model.__dict__: {model.__dict__}\n\tType:{type(model)}')
    print(f'element.__dict__: {elem.__dict__}\n\tType:{type(elem)}')
    print(f'element.parent: {elem.parent.__dict__}\n\tType:{type(elem.parent)}')
    print(f'attr.__dict__: {attr.__dict__}\n\tType:{type(attr)}')
    print(f'attr_ref.__dict__: {attr_ref.__dict__}\n\tType:{type(attr_ref)}')
    print(f'attr_ref.obj_name: {attr_ref.obj_name}')
    print()


def owned_conjugation_definer_scope(owned_conjugation, attr, attr_ref):
    m = get_model(owned_conjugation)  # get the model of the currently processed element
    name = attr_ref.obj_name  # the name of currently looked up element
    print_model_elem(owned_conjugation, m, attr, attr_ref)

    print(f"Owned Relationship Type: {owned_conjugation}")
    mm = get_location(owned_conjugation)
    print(f"mm: {mm}")


def feature_redefinition_definer_scope(redef_relationship, attr, attr_ref):
    """

    MyAttribute:
        ref=[MyInterface|FQN] name=ID ';'
    ;

    The scope providers are Python callables accepting obj, attr, obj_ref:

    * obj : the object representing the start of the search (e.g., a rule, like MyAttribute in the
        example above, or the model)
    * attr : a reference to the attribute (e.g. ref in the first example above)
    * obj_ref : a textx.model.ObjCrossRef - the reference to be resolved

    Parameters
    ----------
    redef_relationship : Redefinition
        Current element being processed.
    attr :
        Reference to the attribute
    attr_ref :
        Reference to be resolved ( textx.model.ObjCrossRef )

    Returns
    -------

    """
    model: kerml.Namespace = get_model(
        redef_relationship)  # get the model of the currently processed element
    element_of_interest = attr_ref.obj_name  # the name of currently looked up element
    print_model_elem(model, redef_relationship, attr, attr_ref)

    # print(f"Redefinition Relationship Type: {type(redef_relationship)}")
    # print(f"m: {model}")
    #
    # for ownedRelationship in model.ownedRelationship:
    #     print(f"Owned Relationship: {ownedRelationship}")
    #     pprint(f"Dict: {ownedRelationship.__dict__}")

    qualified_path = element_of_interest.split("::")
    child: kerml.Feature

    pprint(f"QPath: {qualified_path}")
    pprint(f"Redefinition Name: {redef_relationship.name}")
    pprint(f"Redefinition Parent: {redef_relationship.parent}")

    for child in get_children_of_type("Feature", model):
        if child.name == qualified_path[-1]:
            pprint(f"Child: {child}")
            print(f"\tName: {child.name}")
            print(f"\tParent: {child.parent}\tType: {type(child.parent)}")
            return child
            # if len(qualified_path) > 1:
            #     if child.parent.name == qualified_path[-2]:
            #         return child

    # No feature was found
    metamodel = get_metamodel(model)  # else, create it and store it in the model
    new_feature = metamodel['Feature'](element_of_interest, redef_relationship.parent.name)
    model.ownedRelationship.append(new_feature)
    return new_feature


def owned_specialization_definer_scope(general, attr, attr_ref):
    m = get_model(general)  # get the model of the currently processed element
    name = attr_ref.obj_name  # the name of currently looked up element

    found_general = []
    # If trying to Specialize a Type
    for ownedRel in m.ownedRelationship:
        print(f'Owned Relationship: {ownedRel} - Type: {type(ownedRel)}')
        print(f'Owned Relationship Dict: {ownedRel.__dict__}')
        from kerml import Type
        if isinstance(ownedRel, Type):
            if name == ownedRel.name:
                found_general.append(ownedRel)
        elif 'name' in ownedRel.ownedMemberElement.name and name == ownedRel.ownedMemberElement.name:
            print(f'Attributes:{dir(ownedRel.ownedMemberElement)}')
            found_general.append(ownedRel)

    if len(found_general) > 0:
        return found_general[0]  # if a specialization exists, return it
    else:
        mm = get_metamodel(m)  # else, create it and store it in the model
        general_type = mm['Type'](name, general.parent.name)
        general_type.name = name
        general_type.parent = m
        # TODO: This isn't correct because it will not always be an owned relationship that is
        #  created
        m.ownedRelationship.append(general_type)
        return general_type


class Postponer(object):
    """
    scope provider which forwards to a base scope provider
    and transforms a None to a Postponed.
    Reference resolution will fail if a set of Postponed
    resolutions does not change any more.
    """

    def __init__(self, base=providers.PlainName()):
        self.base = base

    def __call__(self, *args, **kwargs):
        ret = self.base(*args, **kwargs)
        if ret is None:
            return Postponed()
        else:
            return ret
