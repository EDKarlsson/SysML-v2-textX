import json


def element_obj_processor(element):
    pass


class Element(object):
    """
    Attributes:
        aliasId:
        humanId:
        name: /name:String[0..1]
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

    def __init__(self, parent, name, ownedRelationship=None, owningMembership=None, aliasId=[], humanId=None,
                 ownedElement=[]):
        """
        @param parent: TextX Parent
        @param name: TextX Parent
        @param aliasId:
        @param humanId:
        @param ownedElement:
        """
        super(Element, self).__init__()
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


class Relationship(Element):
    def __init__(self, name, parent, humanId=None, ownedRelatedElement=None, source=None, target=None):
        super(Relationship, self).__init__(name=name, parent=parent, humanId=humanId)
        self.source = source
        self.target = target
        self.ownedRelatedElement = ownedRelatedElement
        if self.source is list and self.target is list:
            self.relatedElements = self.source + self.target


class Namespace(Element):
    def __init__(self, name, parent):
        super(Namespace, self).__init__(name=name, parent=parent)


class AnnotatingElement(Element):
    def __init__(self, name, parent):
        super(AnnotatingElement, self).__init__(name=name, parent=parent)
