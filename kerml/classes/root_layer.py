import json


def element_obj_processor(element):
    pass


class Element(object):
    """
    Attributes:
        aliasId: String[0..*] {ordered}
            Various alternative identifiers for this Element.
        humanId: String[0..1] {subsets aliasId}
            An identifier for this Element that is set by the modeler.
        derivedName: String[0..1] (/name)
            [Derived] Primary name of this Element. If the Element is owned by a Namespace, then
            its name is derived as the memberName of the owningMembership of the Element.
        documentation: Documentation[0..*] {subsets ownedAnnotation, ordered}
            [Derived] The ownedAnnotations of this Element that are Documentation, for which the Element
            is the annotatedElement.
        documentationComment: Comment[0..*] {subsetsOwnedAnnotation, ordered}
            [Derived] Comments that document this Element, derived as the documentingComments
            of the documentation of the Element.
        effectiveName:
            [Derived] The effective name to be used for this Element during name resolution within its
            owningNamespace.
        identifier: String
            Globally unique identifier for this Element. Intended to be set by tooling. Immutable.
        ownedAnnotation: Annotation[0..*] {subsets ownedRelationship, annotation, ordered}
            [Derived] The ownedRelationships of this Element that are Annotations, for which this Element
            is the annotatedElement.
        ownedElement: Element[0..*] {ordered}
            [Derived] The Elements owned by this Element, derived as the ownedRelatedElements of the
            ownedRelationships of this Element.
        ownedRelationship:
        ownedTextualRepresentation: TextualRepresentation[0..*] {subsets ownedElement, textualRepresentation}
            [Derived] The textualRepresentations that are ownedElements of this Element.
        owner: Element[0..1]
            [Derived] The owned of this Element, derived as the owningRelatedElement of the
            owningRelationship of this Element, if any.
        owningMembership: Membership[0..1] {subsets owningRelationship}
            The owningRelationship of this Element, if that Relationships is a Membmership.
        owningNamespace: Namespace [0..1] {subsets namespace}
            [Derived] The Namespace that owns this Element, derived as the membershipsOwningNamespace of the
            owningMembership of this Element, if any.
        qualifiedName: String[0..1]
            [Derived] The name of this Element, if it has one, qualified by the name of its owningNamespace, if it has one.
    """

    def __init__(self, parent, name, aliasId=[], humanId=None, ownedRelationship=None, owningMembership=None,
                 ownedElement=[]):
        """
        @param parent: TextX Parent
        @param name: TextX Parent
        @param aliasId:
        @param humanId:
        @param ownedElement:
        @param ownedRelationship:
        @param owningMembership:
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

        # Derived Attributes
        self.identifier = None
        self.owningNamespace = None
        self.documentationComment = None
        self.ownedTextualRepresentation = None
        self.ownedAnnotation = None
        self.documentation = None
        self.derivedName = None

    def escapedName(self):
        return json.dumps(self.name)

    def effectiveName(self):
        return self.name
        # return self.parent.name + '::' + self.name


class Relationship(Element):
    """
    Attributes:
        ownedRelatedElement : Element [0..*] {subsets relatedElement, ordered}
            The relatedElements of this Relationship that are owned by the Relationship.
        owningRelatedElement : Element [0..1] {subsets relatedElement}
            The relatedElement of this Relationship that owns the Relationship, if any.
        relatedElement : Element [2..*] {ordered, nonunique, union}
            [Derived] The Elements that are related by this Relationship, derived as the
            union of the source and target Elements of the Relationship. Every Relationship
            must have at least two relatedElements.
        source : Element [0..*] {subsets relatedElement, ordered}
            The relatedElements from which this Relationship is considered to be directed.
        target : Element [0..*] {subsets relatedElement, ordered}
            The relatedElements to which this Relationship is considered to be directed.
    """

    def __init__(self, name, parent, humanId=None, ownedRelatedElement=None, source=None, target=None):
        super(Relationship, self).__init__(name=name, parent=parent, humanId=humanId)
        self.source = source
        self.target = target
        self.ownedRelatedElement = ownedRelatedElement
        self.relatedElement = []
        if self.source is list:
            self.relatedElement += self.source
        else:
            self.relatedElement.append(self.source)
        if self.target is list:
            self.relatedElement += self.target
        else:
            self.relatedElement.append(self.target)

        self.owningRelatedElement = None


class Namespace(Element):
    def __init__(self, name, parent):
        super(Namespace, self).__init__(name=name, parent=parent)


class AnnotatingElement(Element):
    def __init__(self, name, parent):
        super(AnnotatingElement, self).__init__(name=name, parent=parent)


class Annotation(Relationship):
    def __init__(self, name, parent):
        super(Annotation, self).__init__(name=name, parent=parent)


class ModelComment(AnnotatingElement):
    def __init__(self, parent, name=''):
        super(ModelComment, self).__init__(name=name, parent=parent)


class Documentation(Annotation):
    def __init__(self, parent, name=''):
        super(Documentation, self).__init__(name=name, parent=parent)


class OwnedDocumentation(Documentation):
    def __init__(self, parent, documentingComment, name=''):
        super(OwnedDocumentation, self).__init__(name=name, parent=parent)
        self.documentingComment = documentingComment
