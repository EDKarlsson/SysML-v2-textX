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

    # __slots__ = ["owner", "ownedElement", "ownedRelationship", "owningMembership", "aliasId", "owningNamespace",
    #              "documentationComment", "ownedTextualRepresentation", "ownedAnnotation", "documentation",
    #              "derivedName", "identifier"]

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


class TypeFeaturing(Relationship):
    """
    A TypeFeaturing is a Relationship between a Type and a Feature that is featured by that Type. Every instance in
    the domain of the featureOfType must be classified by the featuringType. This means that sequences that are
    classified by the featureOfType must have a prefix subsequence that is classified by the featuringType.

    Attributes:
        featureOfType : Feature {redefines source}
            The Feature that is featured by the featuringType.
        featuringType : Type {redefines target}
            The Type that features the featureOfType.
        /owningFeatureOfType : Feature [0..1] {subsets featureOfType, owningRelatedElement}
            The Feature that owns this TypeFeaturing and is also the featureOfType.
    """

    # __slots__ = ['parent', 'name', "humanId", "target", "source", "ownedRelatedElement", "owningRelatedElement",
    #              "relatedElement", 'featureOfType', 'featuringType', 'owningFeatureOfType']

    def __init__(self, parent, name, featureOfType=None, featuringType=None):
        """
        @param parent:
        @type parent:
        @param name:
        @type name:
        """
        super(TypeFeaturing, self).__init__(name=name, parent=parent)
        self.featureOfType = featureOfType
        self.featuringType = featuringType


class FeatureMember(Membership, TypeFeaturing):
    """
    FeatureMembership is a Membership for a Feature in a Type that is also a TypeFeaturing Relationship between the
    Feature and the Type.

    Attributes:
        memberFeature : Feature {redefines memberElement, featureOfType}
            The Feature that this FeatureMembership relates to its owningType, making it a ownedFeature of the
            owningType.
        ownedMemberFeature : Feature [0..1] {subsets memberFeature, redefines ownedMemberElement}
            A memberFeature that is owned by this FeatureMembership and hence an ownedFeature of the owningType.
        /owningType : Type {subsets type, redefines membershipOwningNamespace}
            The Type that owns this FeatureMembership.
    """
    # __slots__ = ["parent", "name", "derivedName", "identifier", "featureOfType", "featuringType", "owner",
    #              'memberFeature', 'ownedMemberFeature', "ownedElement", "ownedRelationship", "owningMembership",
    #              "aliasId", "owningNamespace", "documentationComment", "ownedTextualRepresentation", "ownedAnnotation",
    #              "documentation", "owningFeatureOfType"]

    def __init__(self, parent, name, memberFeature=None, ownedMemberFeature=None):
        super(FeatureMember, self).__init__(name=name, parent=parent)
        self.memberName: str = name
        self.memberFeature = memberFeature
        self.ownedMemberFeature = ownedMemberFeature


class Type(Namespace):
    # __slots__ = ['name', 'parent', 'isAbstract', 'importedMembership', 'member', 'ownedMembership']

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


class Specialization(Relationship):
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
    # __slots__ = ["name", "parent", "humanId", "target", "source", "ownedRelatedElement", "owningRelatedElement",
    #              "relatedElement"]

    def __init__(self, name, parent, humanId=None, target=None, source=None,
                 ownedRelatedElement=None, owningRelatedElement=None):
        super(Specialization, self).__init__(name=name, parent=parent, humanId=humanId)
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

        self.owningRelatedElement = owningRelatedElement


class Conjugation(Relationship):
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
    # __slots__ = ["name", "parent", "humanId", "target", "source", "ownedRelatedElement", "owningRelatedElement",
    #              "relatedElement", "conjugatedType", "originalType"]

    def __init__(self, name, parent, humanId=None, target=None, source=None, conjugatedType=None,
                 ownedRelatedElement=None, owningRelatedElement=None, originalType=None):
        super(Conjugation, self).__init__(name=name, parent=parent, humanId=humanId)
        self.source = source
        self.target = target
        self.ownedRelatedElement = ownedRelatedElement
        self.relatedElement = []
        self.conjugatedType = conjugatedType
        self.originalType = originalType
        if self.source is list:
            self.relatedElement += self.source
        else:
            self.relatedElement.append(self.source)
        if self.target is list:
            self.relatedElement += self.target
        else:
            self.relatedElement.append(self.target)

        self.owningRelatedElement = owningRelatedElement


class Disjoining(Relationship):
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
    # __slots__ = ["name", "parent", "humanId", "target", "source", "ownedRelatedElement", "owningRelatedElement",
    #              "relatedElement", "conjugatedType", "originalType"]

    def __init__(self, name, parent, humanId=None, target=None, source=None, conjugatedType=None,
                 ownedRelatedElement=None, owningRelatedElement=None, originalType=None):
        super(Disjoining, self).__init__(name=name, parent=parent, humanId=humanId)
        self.source = source
        self.target = target
        self.ownedRelatedElement = ownedRelatedElement
        self.relatedElement = []
        self.conjugatedType = conjugatedType
        self.originalType = originalType
        if self.source is list:
            self.relatedElement += self.source
        else:
            self.relatedElement.append(self.source)
        if self.target is list:
            self.relatedElement += self.target
        else:
            self.relatedElement.append(self.target)

        self.owningRelatedElement = owningRelatedElement
