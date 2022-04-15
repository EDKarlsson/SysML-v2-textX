from textx.scoping import providers, Postponed

from textx import get_model, get_metamodel


def owned_specialization_definer_scope(general, attr, attr_ref):
    m = get_model(general)  # get the model of the currently processed element
    name = attr_ref.obj_name  # the name of currently looked up element
    # print(f'attr: {attr.__dict__}')
    # print(f'attr_ref: {attr_ref.__dict__}')
    # print()
    # print(f'General: {general.__dict__}')
    # print(f'General Parent: {general.parent.__dict__}')
    # print()
    # print(f'Model: {m.__dict__}')
    # print(f'Name: {name}')
    # print()

    found_general = []
    # If trying to Specialize a Type
    for ownedRel in m.ownedRelationship:
        print(f'Owned Relationship: {ownedRel} - Type: {type(ownedRel)}')
        print(f'Owned Relationship Dict: {ownedRel.__dict__}')
        from kerml import Type
        if isinstance(ownedRel, Type):
            if name == ownedRel.name:
                # print(f"Found name == ownedRel.name : {name} == {ownedRel.name}")
                found_general.append(ownedRel)
        elif 'name' in ownedRel.ownedMemberElement.name and name == ownedRel.ownedMemberElement.name:
            print(f'Attributes:{dir(ownedRel.ownedMemberElement)}')
            # print(f"Found name == ownedMemberElement.name : {name} == {ownedRel.ownedMemberElement.name}")
            found_general.append(ownedRel)
        # print()

    # found_element = list(filter(lambda t: t.name == name, m.ownedRelationship))
    # found_persons = list(filter(lambda p: p.name == name, m.persons))

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
