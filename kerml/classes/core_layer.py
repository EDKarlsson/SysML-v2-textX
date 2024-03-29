try:
    from root_layer import Element, Namespace, Relationship, Membership
except:
    from kerml.classes.root_layer import Element, Namespace, Relationship, Membership

import json


class Type(Namespace):
    """
    A Type is a Namespace that is the most general kind of Element supporting
    the semantics of classification. A Type may be a Classifier or a Feature,
    defining conditions on what is classified by the Type (see also the
    description of isSufficient).

    Attributes
        /directedFeature : Feature [0..*] {subsets feature, ordered}
            The features of this Type that have a non-null direction.
        /endFeature : Feature [0..*] {subsets feature, ordered}
            All features related to this Type by EndFeatureMemberships.
        /feature : Feature [0..*] {subsets member, ordered}
            The memberFeatures of the featureMemberships of this Type.
        /featureMembership : FeatureMembership [0..*] {subsets typedFeaturing, ordered}
            All FeatureMemberships that have the Type as source.
            Each FeatureMembership identifies a Feature of the Type.
        /inheritedFeature : Feature [0..*] {subsets feature, ordered}
            All the memberFeatures of the inheritedMemberships of this Type.
        /inheritedMembership : Membership [0..*] {subsets membership, ordered}
            All Memberships inherited by this Type via Generalization or Conjugation.
        /input : Feature [0..*] {subsets directedFeature, ordered}
            All features related to this Type by FeatureMemberships that have direction in or inout.
        isAbstract : Boolean
            Indicates whether instances of this Type must also be instances of at least one of its
            specialized Types.
        /isConjugated : Boolean
            Indicates whether this Type has an ownedConjugator. (See Conjugation.)
        isSufficient : Boolean
            Whether all things that meet the classification conditions of this Type must
            be classified by the Type. (A Type gives conditions that must be met by whatever
            it classifies, but when isSufficient is false, things may meet those conditions
            but still not be classified by the Type. For example, a Type Car that is not
            sufficient could require everything it classifies to have four wheels, but not all four
            wheeled things would need to be cars. However, if the type Car were sufficient, it
            would classify all four-wheeled things.)
        /multiplicity : Multiplicity [0..1] {subsets member}
            The one member (at most) of this Type that is a Multiplicity, which constrains the
            cardinality of the Type. A multiplicity can be owned or inherited. If it is owned, the
            multiplicity must redefine the multiplicity (if it has one) of any general Type of a
            Generalization of this Type.
        /output : Feature [0..*] {subsets directedFeature, ordered}
            All features related to this Type by FeatureMemberships that have direction out or
            inout.
        /ownedConjugator : Conjugation [0..1] {subsets ownedRelationship, conjugator}
            A Conjugation owned by this Type for which the Type is the originalType.
        /ownedDisjoining : Disjoining [0..*] {subsets ownedRelationship, disjoiningTypeDisjoining}
            The Disjoinings that are among the ownedRelationships of this Type (identify their
            typeDisjoined also as an owningRelatedElement).
        /ownedEndFeature : Feature [0..*] {subsets endFeature, ownedFeature, ordered}
            All endFeatures of this Type that are ownedFeatures.
        /ownedFeature : Feature [0..*] {subsets ownedMember, ordered}
            The ownedMemberFeatures of the ownedFeatureMemberships of this Type.
        /ownedFeatureMembership : FeatureMembership [0..*]
            {subsets ownedMembership, featureMembership, ordered}
            The ownedMemberships of this Type that are FeatureMemberships, for which the Type is
            the owningType. Each such FeatureMembership identifies a feature of the Type.
        /ownedSpecialization : Specialization [0..*]
            {subsets specialization, ownedRelationship, ordered}
            The ownedRelationships of this Type that are Specializations, for which the Type is the
            specific Type.
    """

    def __init__(self, name, parent, humanId=None, aliasId=None, documentation=None,
                 isAbstract=None, isSufficient=None, ownedRelationship=None,
                 importedMembership=None, member=None, membership=None,
                 ownedImport=None, ownedMember=None, ownedMembership=None):
        super(Namespace, self).__init__(name=name, parent=parent,
                                        humanId=humanId, aliasId=aliasId)
        self.isAbstract = isAbstract
        self.importedMembership = importedMembership
        self.ownedMembership = ownedMembership

        self.aliasId = aliasId
        self.member = member
        self.membership = membership
        self.ownedImport = ownedImport
        self.ownedMember = ownedMember
        self.ownedRelationship = ownedRelationship

        self.isSufficient = isSufficient
        self.documentation = documentation


class FeatureElement(Element):
    """
    This is an intermediate class which allows the language to work. There needs to be some
    refactoring done to have this class removed.

    Attributes
        aliasId: String[0..*] {ordered}
            Various alternative identifiers for this Element.
        humanId: String[0..1] {subsets aliasId}
            An identifier for this Element that is set by the modeler.
        derivedName: String[0..1] (/name)
            [Derived] Primary name of this Element. If the Element is owned by a Namespace, then
            its name is derived as the memberName of the owningMembership of the Element.
        documentation: Documentation[0..*] {subsets ownedAnnotation, ordered}
            [Derived] The ownedAnnotations of this Element that are Documentation, for which the
            Element is the annotatedElement.
        documentationComment: Comment[0..*] {subsetsOwnedAnnotation, ordered}
            [Derived] Comments that document this Element, derived as the documentingComments of
            the documentation of the Element.
        effectiveName
            [Derived] The effective name to be used for this Element during name resolution within
            its owningNamespace.
        identifier: str
            Globally unique identifier for this Element. Intended to be set by tooling. Immutable.
        ownedAnnotation: Annotation[0..*] {subsets ownedRelationship, annotation, ordered}
            [Derived] The ownedRelationships of this Element that are Annotations, for which this
            Element is the annotatedElement.
        ownedElement: Element[0..*] {ordered}
            [Derived] The Elements owned by this Element, derived as the ownedRelatedElements of the
            ownedRelationships of this Element.
        ownedRelationship: Relationship [0..*] {subsets relationship, ordered}
            The Relationships for which this Element is the owningRelatedElement.
        ownedTextualRepresentation: TextualRepresentation[0..*]
            {subsets ownedElement, textualRepresentation}
            [Derived] The textualRepresentations that are ownedElements of this Element.
        owner: Element[0..1]
            [Derived] The owned of this Element, derived as the owningRelatedElement of the
            owningRelationship of this Element, if any.
        owningMembership: Membership[0..1] {subsets owningRelationship}
            The owningRelationship of this Element, if that Relationships is a Membership.
        owningNamespace: Namespace [0..1] {subsets namespace}
            [Derived] The Namespace that owns this Element, derived as the membershipsOwningNamespace
            of the owningMembership of this Element, if any.
        qualifiedName: String[0..1]
            [Derived] The name of this Element, if it has one, qualified by the name of its
            owningNamespace, if it has one.
    """

    def __init__(self, parent, name, ownedElement: Element, aliasId=None,
                 humanId=None, ownedRelationship=None,
                 owningMembership=None, owningNamespace=None,
                 documentationComment=None,
                 ownedTextualRepresentation=None, ownedAnnotation=None,
                 documentation=None, derivedName=None, ):
        super(Element, self).__init__(name=name, parent=parent, humanId=humanId,
                                      aliasId=aliasId)
        self.owner: Element = self.parent
        self.ownedElement: Element = ownedElement
        self.ownedRelationship: Relationship = ownedRelationship
        self.owningMembership: Membership = owningMembership
        if humanId is not None:
            self.aliasId = [self.humanId] + aliasId
        else:
            self.aliasId = list(aliasId)

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
    A TypeFeaturing is a Relationship between a Type and a Feature that is featured by that Type.
    Every instance in the domain of the featureOfType must be classified by the featuringType.
    This means that sequences that are classified by the featureOfType must have a prefix
    subsequence that is classified by the featuringType.

    Attributes
        featureOfType : Feature {redefines source}
            The Feature that is featured by the featuringType.
        featuringType : Type {redefines target}
            The Type that features the featureOfType.
        /owningFeatureOfType : Feature [0..1] {subsets featureOfType, owningRelatedElement}
            The Feature that owns this TypeFeaturing and is also the featureOfType.
    """

    def __init__(self, parent, name, humanId=None, featureOfType=None, featuringType=None):
        super(TypeFeaturing, self).__init__(name=name, parent=parent, humanId=humanId)
        self.featureOfType = featureOfType
        self.featuringType = featuringType


class FeatureMember(Membership, TypeFeaturing):
    """
    FeatureMembership is a Membership for a Feature in a Type that is also a TypeFeaturing
    Relationship between the Feature and the Type.

    Attributes
        memberFeature : Feature {redefines memberElement, featureOfType}
            The Feature that this FeatureMembership relates to its owningType, making it a
            ownedFeature of the owningType.
        ownedMemberFeature : Feature [0..1] {subsets memberFeature, redefines ownedMemberElement}
            A memberFeature that is owned by this FeatureMembership and hence an ownedFeature of
            the owningType.
        /owningType : Type {subsets type, redefines membershipOwningNamespace}
            The Type that owns this FeatureMembership.
    """

    def __init__(self, parent, name, memberFeature=None, ownedMemberFeature=None,
                 memberElement=None, ownedMemberElement=None):
        super(FeatureMember, self).__init__(name=name, parent=parent, memberElement=memberElement,
                                            ownedMemberElement=ownedMemberElement)
        self.memberName: str = name
        self.memberFeature = memberFeature
        self.ownedMemberFeature = ownedMemberFeature


class Specialization(Relationship):
    """
    Attributes
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

    def __init__(self, name, parent, humanId=None, target=None, source=None,
                 ownedRelatedElement=None, owningRelatedElement=None, specific=None, general=None):
        super(Specialization, self).__init__(name=name, parent=parent,
                                             humanId=humanId)
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
        self.specific = specific
        self.general = general


class Conjugation(Relationship):
    """
    Attributes
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

    def __init__(self, name, parent, humanId=None, target=None, source=None,
                 conjugatedType=None, ownedRelatedElement=None, owningRelatedElement=None,
                 originalType=None):
        super(Conjugation, self).__init__(name=name, parent=parent,
                                          humanId=humanId)
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
    Attributes
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

    def __init__(self, name, parent, humanId=None, target=None, source=None,
                 conjugatedType=None, ownedRelatedElement=None, owningRelatedElement=None,
                 originalType=None):
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


class Feature(Type):
    """
    A Feature is a Type that classifies sequences of multiple things (in the universe).
    These must concatenate a sequence drawn from the intersection of the Feature's
    featuringTypes (domain) with a sequence drawn from the intersection of its types
    (co-domain), treating (co)domains as sets of sequences. The domain of Features that
    do not have any featuringTypes is the same as if it were the library Type Anything.
    A Feature's types include at least Anything, which can be narrowed to other
    Classifiers by Redefinition.

    In the simplest cases, a Feature's featuringTypes and types are Classifiers, its
    sequences being pairs (length = 2), with the first element drawn from the Feature's
    domain and the second element from its co-domain (the Feature "value"). Examples
    include cars paired with wheels, people paired with other people, and cars paired
    with numbers representing the car length.

    Since Features are Types, their featuringTypes and types can be Features. When both
    are, Features classify sequences of at least four elements (length > 3), otherwise
    at least three (length > 2). The featuringTypes of nested Features are Features.

    The values of a Feature with chainingFeatures are the same as values of the last
    Feature in the chain, which can be found by starting with values of the first
    Feature, then from those values to values of the second feature, and so on, to
    values of the last feature.

    Attributes:
        /chainingFeature : Feature [0..*] {ordered, nonunique}
            The Features that are chained together to determine the values of this Feature,
            derived from the chainingFeatures of the ownedFeatureChainings of this Feature,
            in the same order. The values of a Feature with chainingFeatures are the same
            as values of the last Feature in the chain, which can be found by starting with
            the values of the first Feature (for each instance of the original Feature's domain),
            then on each of those to the values of the second Feature in chainingFeatures,
            and so on, to values of the last Feature. The Features related to a Feature by a
            FeatureChaining are identified as its chainingFeatures.
        direction : FeatureDirectionKind [0..1]
            Determines how values of this Feature are determined or used (see FeatureDirectionKind).
        /endOwningType : Type [0..1] {subsets typeWithEndFeature, owningType}
            The Type that is related to this Feature by an EndFeatureMembership in which the
            Feature is an ownedMemberFeature.
        /featuringType : Type [0..*] {ordered}
        isComposite : Boolean
            Whether the Feature is a composite feature of its featuringType. If so, the values
            of the Feature cannot exist after the instance of the featuringType no longer does.
        isDerived : Boolean
            Whether the values of this Feature can always be computed from the values of other Features.
        isEnd : Boolean
            Whether or not the this Feature is an end Feature, requiring a different interpretation
            of the multiplicity of the Feature. An end Feature is always considered to map each
            domain entity to a single co-domain entity, whether or not a Multiplicity is given
            for it. If a Multiplicity is given for an end Feature, rather than giving the co-domain
            cardinality for the Feature as usual, it specifies a cardinality constraint for navigating
            across the endFeatures of the featuringType of the end Feature. That is, if a Type
            has n endFeatures, then the Multiplicity of any one of those end Features constrains
            the cardinality of the set of values of that Feature when the values of the other n-1
            end Features are held fixed.
        isOrdered : Boolean
            Whether an order exists for the values of this Feature or not.
        isPortion : Boolean
            Whether the values of this Feature are contained in the space and time of instances
            of the Feature's domain.
        isReadOnly : Boolean
            Whether the values of this Feature can change over the lifetime of an instance of
            the domain.
        isUnique : Boolean
            Whether values for this Feature must have no duplicates or not.
        /ownedFeatureChaining : FeatureChaining [0..*] {subsets sourceRelationship, ownedRelationship, ordered}
            The FeatureChainings that are among the ownedRelationships of this Feature
            (identify their featureChained also as an owningRelatedElement).
        /ownedRedefinition : Redefinition [0..*] {subsets ownedSubsetting}
            The ownedSubsettings of this Feature that are Redefinitions, for which the Feature
            is the redefiningFeature.
        /ownedSubsetting : Subsetting [0..*] {subsets ownedSpecialization, subsetting}
            The ownedGeneralizations of this Feature that are Subsettings, for which the Feature
            is the subsettingFeature.

        /ownedTypeFeaturing : TypeFeaturing [0..*] {subsets ownedRelationship, typeFeaturing, ordered}
            The ownedRelationships of this Feature that are TypeFeaturings, for which the Feature is the featureOfType.
        /ownedTyping : FeatureTyping [0..*] {subsets ownedSpecialization, typing, ordered}
            The ownedGeneralizations of this Feature that are FeatureTypings, for which the Feature is the typedFeature.
        owningFeatureMembership : FeatureMembership [0..1] {subsets owningMembership, featureMembership}
            The FeatureMembership that owns this Feature as an ownedMemberFeature, determining its owningType.
        /owningType : Type [0..1] {subsets typeWithFeature, owningNamespace, featuringType}
            The Type that is the owningType of the owningFeatureMembership of this Type.
        /type : Type [1..*] {ordered}
            Types that restrict the values of this Feature, such that the values must be instances of all the types. The types of a
            Feature are derived from its ownedFeatureTypings and the types of its ownedSubsettings.
    """

    def __init__(self, name, parent, humanId=None, direction=None, isAbstract=None,
                 isSufficient=None, ownedRelationship=None, owningFeatureMembership=None,
                 isEnd=False, isComposite=False, isDerived=False, isOrdered=False, isPortion=False,
                 isUnique=False, isReadOnly=False):
        super(Feature, self).__init__(name=name, parent=parent, humanId=humanId,
                                      ownedRelationship=ownedRelationship)
        self.direction = direction
        self.isAbstract = isAbstract
        self.isSufficient = isSufficient
        self.isEnd = isEnd
        self.isComposite = isComposite
        self.isDerived = isDerived
        self.isOrdered = isOrdered
        self.isPortion = isPortion
        self.isUnique = isUnique
        self.isReadOnly = isReadOnly
        self.owningFeatureMembership = owningFeatureMembership


class Multiplicity(Feature):
    """
    A Multiplicity is a Feature whose co-domain is a set of natural numbers that includes the
    number of sequences determined below, based on the kind of typeWithMultiplicity:

    - Classifiers: minimal sequences (the single length sequences of the Classifier).
    - Features: sequences with the same feature-pair head.

    In the case of Features with Classifiers as domain and co-domain, these sequences are pairs,
    with the first element in a single-length sequence of the domain Classifier (head of the pair),
    and the number of pairs with the same first element being among the Multiplicity co-domain
    numbers.

    Multiplicity co-domains (in models) can be specified by Expression that might vary in their
    results. If the typeWithMultiplicity is a Classifier, the domain of the Multiplicity shall be
    Anything. If the typeWithMultiplicity is a Feature, the Multiplicity shall have the same domain
    as the typeWithMultiplicity.
    """

    def __init__(self, name, parent, humanId=None):
        super(Multiplicity, self).__init__(name=name, parent=parent, humanId=humanId)


class Classifier(Type):
    """
    A Classifier is a Type for model elements that classify:

    - Things (in the universe) regardless of how Features relate them. These are sequences of
      exactly one thing (sequence of length 1).
    - How the above things are related by Features. These are sequences of multiple things
      (length > 1).

    Classifiers that classify relationships (sequence length > 1) must also classify the things at
    the end of those sequences (sequence length =1). Because of this, Classifiers specializing
    Features cannot classify anything (any sequences).

    Attributes
        /ownedSubclassification : Subclassification [0..*] {subsets ownedSpecialization}
            The ownedSpecializations of this Classifier that are Subclassifications, for which this
            Classifier is the subclassifier.
        name : str
            textX `name` of the element
        parent : str
            textX `parent` of the element
    """

    def __init__(self, name, parent, humanId=None, ownedSubclassification=None, isAbstract=False,
                 isSufficient=False, ownedRelationship=None, documentation=None):
        super(Classifier, self).__init__(name=name, parent=parent, humanId=humanId,
                                         isAbstract=isAbstract, isSufficient=isSufficient,
                                         ownedRelationship=ownedRelationship,
                                         documentation=documentation)
        self.ownedSubclassification = ownedSubclassification


class Subclassification(Specialization):
    """
    Subclassification is Specialization in which both the specific and general Types are
    Classifiers. This means all instances of the specific Classifier are also instances of the
    general Classifier.

    Attributes
        /owningClassifier : Classifier [0..1] {redefines owningType}
            The Classfier that owns this Subclassification relationship, which must also be its
            subclassifier.
        subclassifier : Classifier {redefines specific}
            The more specific Classifier in this Subclassification.
        superclassifier : Classifier {redefines general}
            The more general Classifier in this Subclassification.
    """

    def __init__(self, name, parent, owningClassifier=None, subclassifier=None,
                 superclassifier=None):
        super(Subclassification, self).__init__(name, parent)
        self.owningClassifier = owningClassifier
        self.subclassifier = subclassifier
        self.superclassifier = superclassifier


class Subsetting(Specialization):
    """
    Subsetting is Generalization in which the specific and general Types that are Features. This
    means all values of the subsettingFeature (on instances of its domain, i.e., the intersection
    of its featuringTypes) are values of the subsettedFeature on instances of its domain. To
    support this, the domain of the subsettingFeature must be the same or specialize (at least
    indirectly) the domain of the subsettedFeature (via Generalization), and the range (
    intersection of a Feature's types) of the subsettingFeature must specialize the range of the
    subsettedFeature. The subsettedFeature is imported into the owningNamespace of the
    subsettingFeature (if it is not already in that namespace), requiring the names of the
    subsettingFeature and subsettedFeature to be different.

    Attributes
        /owningFeature : Feature {subsets subsettingFeature, redefines owningType}
            The Feature that owns this Subsetting relationship, which must also be its
            subsettingFeature.
        subsettedFeature : Feature {redefines general}
            The Feature that is subsetted by the subsettingFeature of this Subsetting.
        subsettingFeature : Feature {redefines specific}
            The Feature that is a subset of the subsettedFeature of this Subsetting.
    """

    def __init__(self, name, parent, humanId=None, owningFeature=None, subsettedFeature=None,
                 subsettingFeature=None, ownedRelatedElement=None, owningRelatedElement=None,
                 specific=None, general=None):
        super(Subsetting, self).__init__(name=name, parent=parent, humanId=humanId,
                                         ownedRelatedElement=ownedRelatedElement,
                                         owningRelatedElement=owningRelatedElement,
                                         specific=specific, general=general)
        self.owningFeature = owningFeature
        self.subsettedFeature = subsettedFeature
        self.subsettingFeature = subsettingFeature


class Redefinition(Subsetting):
    """
    Redefinition specializes Subsetting to require the redefinedFeature and the redefiningFeature
    to have the same values (on each instance of the domain of the redefiningFeature). This means
    any restrictions on the redefiningFeature, such as type or multiplicity, also apply to the
    redefinedFeature (on each instance of the owningType of the redefining Feature), and vice
    versa. The redefinedFeature might have values for instances of the owningType of the
    redefiningFeature, but only as instances of the owningType of the redefinedFeature that
    happen to also be instances of the owningType of the redefiningFeature. This is supported by
    the constraints inherited from Subsetting on the domains of the redefiningFeature and
    redefinedFeature. However, these constraints are narrowed for Redefinition to require the
    owningTypes of the redefiningFeature and redefinedFeature to be different and the
    redefinedFeature to not be imported into the owningNamespace of the redefiningFeature. This
    enables the redefiningFeature to have the same name as the redefinedFeature if desired.

    Attributes
        redefinedFeature : Feature {redefines subsettedFeature}
            The Feature that is redefined by the redefiningFeature of this Redefinition.
        redefiningFeature : Feature {redefines subsettingFeature}
            The Feature that is redefining the redefinedFeature of this Redefinition.
    """

    def __init__(self, name, parent, humanId=None, redefinedFeature=None, redefiningFeature=None,
                 specific=None, general=None):
        super(Redefinition, self).__init__(name=name, parent=parent, humanId=humanId,
                                           specific=specific, general=general)
        self.redefinedFeature = redefinedFeature
        self.redefiningFeature = redefiningFeature


class FeatureTyping(Specialization):
    """
    FeatureTyping is Specialization in which the specific Type is a Feature. This means the set
    of instances of the (specific) typedFeature is a subset of the set of instances of the (
    general) type. In the simplest case, the type is a Classifier, whereupon the typedFeature
    subset has instances interpreted as sequences ending in things (in the modeled universe) that
    are instances of the Classifier.

    Attributes
        /owningFeature : Feature [0..1] {subsets typedFeature, redefines owningType}
            The Feature that owns this FeatureTyping (which must also be the typedFeature).
        type : Type {redefines general}
            The Type that is being applied by this FeatureTyping.
        typedFeature : Feature {redefines specific}
            The Feature that has its Type determined by this FeatureTyping.
    """

    def __init__(self, name, parent, humanId=None, general=None, typedFeature=None):
        super(FeatureTyping, self).__init__(name=name, parent=parent, humanId=humanId)
        self.general = general
        self.typedFeature = typedFeature


class FeatureChaining(Relationship):
    """
    FeatureChaining is a Relationship that makes its target Feature one of the chainingFeatures of
    its owning Feature.

    Attributes
        chainingFeature : Feature {redefines target}
             The Feature whose values partly determine values of featureChained, as described in
             Feature::chainingFeature.
        /featureChained : Feature {redefines source, owningRelatedElement}
            The Feature whose values are partly determined by values of the chainingFeature, as
            described in Feature::chainingFeature.
    """

    def __init__(self, name, parent, humanId=None, chainingFeature=None):
        super(FeatureChaining, self).__init__(name=name, parent=parent, humanId=humanId)
        self.chainingFeature = chainingFeature


class EndFeatureMembership(FeatureMember):
    """
    EndFeatureMembership is a FeatureMembership that requires its memberFeature be owned and have
    isEnd = true.

    Attributes
        ownedMemberFeature : Feature {redefines ownedMemberFeature}
    """

    def __init__(self, name, parent):
        super(EndFeatureMembership, self).__init__(name=name, parent=parent)
