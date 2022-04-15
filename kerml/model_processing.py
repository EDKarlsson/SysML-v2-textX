from pprint import pprint
from textx.scoping import providers, Postponed
from textx import get_model, get_metamodel, get_location


def print_model_elem(elem, model, attr, attr_ref):
    print(f'attr.__dict__: {attr.__dict__}')
    print(f'attr_ref.__dict__: {attr_ref.__dict__}')
    print()
    print(f'element.__dict__: {elem.__dict__}')
    print(f'element.parent: {elem.parent.__dict__}')
    print()
    print(f'model.__dict__: {model.__dict__}')
    print(f'attr_ref.obj_name: {attr_ref.obj_name}')
    print()


def owned_conjugation_definer_scope(owned_conjugation, attr, attr_ref):
    m = get_model(owned_conjugation)  # get the model of the currently processed element
    name = attr_ref.obj_name  # the name of currently looked up element
    print_model_elem(owned_conjugation, m, attr, attr_ref)
    found_relationships = []
    print(f"Owned Relationship Type: {owned_conjugation}")
    mm = get_location(owned_conjugation)
    print(f"mm: {mm}")
    print(f"mm.__dict__: {mm.__dict__}")


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
