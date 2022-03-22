import json


class Element(object):
    """
    Attributes:
        aliasId:
        humanId:
        name:
        ownedRelationship:
        owningMembership:
        parent:
        derivedName: [Derived]
        documentation: [Derived]
        documentationComment: [Derived]
        effectiveName: [Derived]
        identifier: [Derived]
        ownedAnnotation: [Derived]
        ownedElement: [Derived]
        ownedTextualRepresentation: [Derived]
        owner: [Derived]
        owningNamespace: [Derived]
        qualifiedName: [Derived]
    """

    def __init__(self, parent, name, ownedRelationship=None, owningMembership=None, aliasId=[], humanId=None, ownedElement=[]):
        """
        @param parent:
        @param name:
        @param aliasId:
        @param humanId:
        @param ownedElement:
        """
        self.name = name
        self.parent = parent
        self.owner = self.parent
        self.humanId = humanId
        self.ownedElement = ownedElement
        self.ownedRelationship = ownedRelationship
        self.owningMembership = owningMembership
        self.aliasId = [self.humanId] + aliasId

        # Need to add logic to these
        if hasattr(self.parent, 'name'):
            if self.parent.name == '':
                self.qualifiedName = self.name
            else:
                self.qualifiedName = self.parent.name + '::' + self.name
        else:
            self.qualifiedName = self.name
        self.effectiveName = self.effectiveName()

    def escapedName(self):
        return json.dumps(self.name)

    def effectiveName(self):
        return self.name
        # return self.parent.name + '::' + self.name


class Relationship(object):
    def __init__(self, name, parent, source, target):
        self.parent = parent
        self.name = name
        self.source = source
        self.target = target
        self.ownedRelatedElements = None
        self.ownedRelationship = None
