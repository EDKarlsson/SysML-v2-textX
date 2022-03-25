try:
    from root_layer import Element, Namespace, Relationship, Membership
except:
    from kerml.classes.root_layer import Element, Namespace, Relationship, Membership

import json


class FeatureElement(Element):
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

    def __init__(self, parent, name, ownedElement: Element, aliasId=None, humanId=None, ownedRelationship=None,
                 owningMembership=None, owningNamespace=None, documentationComment=None,
                 ownedTextualRepresentation=None, ownedAnnotation=None, documentation=None, derivedName=None, ):
        """
        @param owningNamespace:
        @type owningNamespace:
        @param parent: TextX Parent
        @param name: TextX Parent
        @param aliasId:
        @param humanId:
        @param ownedElement:
        @param ownedRelationship:
        @param owningMembership:
        """
        super(Element, self).__init__(name=name, parent=parent, humanId=humanId, aliasId=aliasId)
        self.owner: Element = self.parent
        self.ownedElement: Element = ownedElement
        self.ownedRelationship: Relationship = ownedRelationship
        self.owningMembership: Membership = owningMembership
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
        self.owningNamespace: Namespace = owningNamespace
        self.documentationComment = documentationComment
        self.ownedTextualRepresentation = ownedTextualRepresentation
        self.ownedAnnotation = ownedAnnotation
        self.documentation = documentation
        self.derivedName = derivedName

    def escapedName(self):
        return json.dumps(self.name)

    def effectiveName(self):
        return self.name
        # return self.parent.name + '::' + self.name


class Type(Namespace):
    def __init__(self, name, parent, humanId=None, aliasId=None, isAbstract=None, isSufficient=None,
                 documentation=None, ownedRelationship=None,

                 importedMembership=None, member=None, membership=None,
                 ownedImport=None, ownedMember=None, ownedMembership=None):
        super(Namespace, self).__init__(name=name, parent=parent, humanId=humanId, aliasId=aliasId)
        self.name = name
        self.parent = parent
        self.humanId = humanId
        self.aliasId = aliasId
        self.ownedRelationship = ownedRelationship
        self.importedMembership = importedMembership
        self.member = member
        self.membership = membership
        self.ownedImport = ownedImport
        self.ownedMember = ownedMember
        self.ownedMembership = ownedMembership
