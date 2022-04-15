try:
    from core_layer import Classifier, Feature, Multiplicity, FeatureMember
    from root_layer import Element, Namespace, Relationship, Membership, Import, AnnotatingElement
except:
    from kerml.classes.core_layer import Classifier, Feature, Multiplicity, FeatureMember
    from kerml.classes.root_layer import Element, Namespace, Relationship, Membership, Import, \
        AnnotatingElement


class Class(Classifier):
    """
    A Class is a Classifier of things (in the universe) that can be distinguished without regard
    to how they are related to other things (via Features). This means multiple things classified
    by the same Class can be distinguished, even when they are related other things in exactly
    the same way.

    Constraints
        classClassifiesOccurrence:
            [no documentation]
            allSupertypes()->includes(Kernel Library::Occurrence)
    """

    def __init__(self, name, parent):
        super(Class, self).__init__(name=name, parent=parent)
        self.name = name
        self.parent = parent


class DataType(Classifier):
    """
    A DataType is a Classifier of things (in the universe) that can only be distinguished by how
    they are related to other things (via Features).

    This means multiple things classified by the same DataType:
      - Cannot be distinguished when they are related to other things in exactly the
        same way, even when they are intended to be about the same thing.
      - Can be distinguished when they are related to other things in different ways, even when
        they are intended to be about the same thing.

    Constraints
        datatypeClassifiesDataValue:
            [no documentation]
            allSupertypes()->includes(Kernel Library::DataValue)
    """

    def __init__(self, name, parent):
        super(DataType, self).__init__(name=name, parent=parent)
        self.name = name
        self.parent = parent


class Structure(Class):
    """
    A Structure is a Class of objects in the modeled universe that are primarily structural in
    nature. While an Object is not itself behavioral, it may be involved in and acted on by
    Behaviors, and it may be the performer of some of them.

    Constraints
        structureClassifiesObject:
            [no documentation]
            allSupertypes()->includes(Kernel Library::Object)
    """

    def __init__(self, name, parent):
        super(Structure, self).__init__(name=name, parent=parent)
        self.name = name
        self.parent = parent


class Association(Classifier, Relationship):
    """
    An Association is a Relationship and a Classifier to enable classification of links between
    things (in the universe). The co-domains (types) of the associationEnd Features are the
    relatedTypes, as co-domain and participants (linked things) of an Association identify each
    other.

    Attributes
        /associationEnd : Feature [2..*]
            {redefines endFeature}
            The features of the Association that identifying the things that can be related by it.
            An Association must have at least two associationEnds. When it has exactly two, the
            Association is called a binary Association.
        /relatedType : Type [2..*]
            {redefines relatedElement, ordered, nonunique, union}
            The types of the endFeatures of the Association, which are the relatedElements of the
            Association considered as a Relationship.
        /sourceType : Type [0..1]
            {subsets relatedType, redefines source}
            The source relatedType for this Association. If this is a binary Association, then the
            sourceType is the first relatedType, and the first associationEnd of the Association
            must redefine the source Feature of the Association BinaryLink from the Kernel Library.
            If this Association is not binary, then it has no sourceType.
        /targetType : Type [1..*]
            {subsets relatedType, redefines target}
            The target relatedTypes for this Association. This includes all the relatedTypes other
            than the sourceType. If this is a binary Association, then the associationEnds
            corresponding to the relatedTypes must all redefine the target Feature of the
            Association BinaryLink from the Kernel Library.

    Constraints
        AssociationLink:
            [no documentation]

            let numend : Natural = associationEnd->size() in
                allSupertypes()->includes(
                    if numend = 2 then Kernel Library::BinaryLink
                    else Kernel Library::Link)

        associationClassifiesLink:
            [no documentation]
            allSupertypes()->includes(Kernel Library::Link)
        AssociationStructureIntersection:
            [no documentation]
            oclIsKindOf(Structure) = oclIsKindOf(AssociationStructure)
        associationRelatedTypes:
            [no documentation]
            relatedTypes = associationEnd.type
    """

    def __init__(self, name, parent, humanId=None, associationEnd=None, relatedType=None,
                 sourceType=None, targetType=None):
        super(Association, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId
        self.associationEnd = associationEnd
        self.relatedType = relatedType
        self.sourceType = sourceType
        self.targetType = targetType


class AssociationStructure(Association, Structure):
    """
    No Description

    Constraints
        associationStructureClassifiesLinkObject:
            [no documentation]
            allSupertypes()->includes(Kernel Library::LinkObject)
    """

    def __init__(self, name, parent, humanId=None):
        super(AssociationStructure, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class Connector(Feature, Relationship):
    """
    A Connector is a usage of Associations, with links restricted to instances of the Type in
    which it is used (domain of the Connector). Associations restrict what kinds of things might
    be linked. The Connector further restricts these links to between values of two Features on
    instances of its domain.

    Attributes
        /association : Association [1..*]
            {redefines type}

            The Associations that type the Connector.
        /connectorEnd : Feature [2..*]
            {redefines endFeature}

            These are the ends of the Connector, which show what Features it relates. The
            connectorEnds of a Connector are the features of the Connector that redefine the end
            Features of the Connector association.

        isDirected : Boolean
            Whether or not the Connector should be considered to have a direction from source to
            target.

        /relatedFeature : Feature [2..*]
            {redefines relatedElement, ordered, nonunique, union}

            The Features that are related by this Connector considered as a Relationship, derived
            as the subsetted Features of the connectorEnds of the Connector.

        /sourceFeature : Feature [0..1]
            {subsets relatedFeature, redefines source}

            The source relatedFeature for this Connector. If this is a binary Connector, then the
            sourceFeature is the first relatedFeature, and the first end Feature of the Connector
            must redefine the source Feature of the Connector binaryLinks from the Kernel Library.
            If this Connector is not binary, then it has no sourceFeature.

        /targetFeature : Feature [1..*]
            {subsets relatedFeature, redefines target}

            The target relatedFeatures for this Connector. This includes all the relatedFeatures
            other than the sourceFeature. If this is a binary Connector, then the end Feature
            corresponding to the targetFeature must redefine the target Feature of the Connector
            binaryLinks from the Kernel Library.

    Constraints
        connectorEndRedefinition
            For each association of a Connector, each associationEnd must be redefined by a
            different connectorEnd of the Connector.

            association->forAll(a |
                a.associationEnd->forAll(ae |
                    connectorEnd->one(ce |
                        ce.ownedRedefinition.redefinedFeature->includes(ae))))

        connectorTargetFeature
            The targetFeatures of a Connector are the relatedFeatures other than the sourceFeature.

            targetFeature =
                if sourceFeature = null then relatedFeature
                else relatedFeature->excluding(sourceFeature)
                endif

        connectorConnectorEnd
            The connectorEnds of a Connector are its endFeatures.

            connectorEnd = feature->select(isEnd)

        connectorRelatedFeatures
            The relatedFeatures of a Connector are the subsetted Features of its connectorEnds.
            relatedFeature = connectorEnd.ownedSubsetting.subsettedFeature connectorFeaturingType
            Each relatedFeature of a Connector must have some featuringType of the Connector as a
            direct or indirect featuringType (where a Feature with no featuringType is treated as
            if the Classifier Base::Anything was its featuringType).

            relatedFeature->forAll(f |
                if featuringType->isEmpty() then f.isFeaturedWithin(null)
                else featuringType->exists(t | f.isFeaturedWithin(t))
                endif)

        connectorSourceFeature
            If this is a binary Connector, then the sourceFeature is the first relatedFeature.
            If this Connector is not binary, then it has no sourceFeature.

            sourceFeature =
                if relatedFeature->size() = 2 then relatedFeature->at(1)
                else null
                endif
    """

    def __init__(self, name, parent, humanId=None, isDirected=False, association=None,
                 connectorEnd=None, relatedFeature=None, sourceFeature=None, targetFeature=None):
        super(Connector, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId

        self.isDirected = isDirected
        self.association = association
        self.connectorEnd = connectorEnd
        self.relatedFeature = relatedFeature
        self.sourceFeature = sourceFeature
        self.targetFeature = targetFeature


class BindingConnector(Connector):
    """
    A Binding Connector is a binary Connector that requires its relatedFeatures to identify the
    same things (have the same values).
    """

    def __init__(self, name, parent, humanId=None):
        super(BindingConnector, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class Succession(Connector):
    """
    A Succession is a binary Connector that requires its relatedFeatures to happen separately in
    time. A Succession must be typed by the Association HappensBefore from the Kernel Model
    Library (or a specialization of it).

    Attributes
        /effectStep : Step [0..*]
            Steps that represent occurrences that are side effects of the transitionStep occurring.
        /guardExpression : Expression [0..*]
            Expressions that must evaluate to true before the transitionStep can occur.
        /transitionStep : Step [0..1] {subsets ownedFeature}
            A Step that is typed by the Behavior TransitionPerformance (from the Model Library)
            that has this Succession as its transitionLink.
        /triggerStep : Step [0..*]
            Steps that map incoming events to the timing of occurrences of the transitionStep.
            The values of triggerStep subset the list of acceptable events to be received by a
            Behavior or the object that performs it.
"""

    def __init__(self, name, parent, humanId=None, effectStep=None, guardExpression=None,
                 transitionStep=None, triggerStep=None):
        super(Succession, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId

        self.effectStep = effectStep
        self.guardExpression = guardExpression
        self.transitionStep = transitionStep
        self.triggerStep = triggerStep


class Behavior(Class):
    """
    A Behavior coordinates occurrences of other Behaviors, as well as changes in objects. Behaviors
    can be decomposed into Steps and be characterized by parameters.

    Attributes
        /parameter : Feature [0..*] {redefines directedFeature, ordered}
            The parameters of this Behavior, which are all its directedFeatures, whose values are
            passed into and/or out of a performance of the Behavior.
        /step : Step [0..*] {subsets feature}
            The Steps that make up this Behavior.

    Constraints
        behaviorClassifiesPerformance:
            [no documentation]
            allSupertypes()->includes(Kernel Library::Performance)
    """

    def __init__(self, name, parent, parameter=None, step=None):
        super(Behavior, self).__init__(name=name, parent=parent)
        self.name = name
        self.parent = parent

        self.parameter = parameter
        self.step = step


class Step(Feature):
    """
    A Step is a Feature that is typed by one or more Behaviors. Steps may be used by one Behavior
    to coordinate the performance of other Behaviors, supporting the steady refinement of
    behavioral descriptions. Steps can be ordered in time and can be connected using ItemFlows to
    specify things flowing between their parameters.

    Attributes
        /behavior : Behavior [1..*] {redefines type, ordered}
            The Behaviors that type this Step.
        /parameter : Feature [0..*] {redefines directedFeature, ordered}
            The parameters of this Expression, which are all its directedFeatures, whose values
            are passed into and/or out of a performance of the Behavior.
    """

    def __init__(self, name, parent, humanId=None, behavior=None, parameter=None):
        super(Step, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId

        self.behavior = behavior
        self.parameter = parameter


class ParameterMembership(FeatureMember):
    """
    A ParameterMembership is a FeatureMembership that identifies its memberFeature as a
    parameter, which is always owned, and must have a direction. A ParameterMembership must be
    owned by a Behavior or a Step.

    Attributes
        memberParameter : Feature {redefines memberFeature}
            The Feature that is identified as a parameter by this ParameterMembership, which must
            be the ownedMemberParameter.
        ownedMemberParameter : Feature {redefines ownedMemberFeature}
            The Feature that is identified as a parameter by this ParameterMembership, which is
            always owned by the ParameterMembership.
    """

    def __init__(self, name, parent, memberParameter=None, ownedMemberParameter=None):
        super(ParameterMembership, self).__init__(name=name, parent=parent)
        self.name = name
        self.parent = parent
        self.memberParameter = memberParameter
        self.ownedMemberParameter = ownedMemberParameter


class Function(Behavior):
    def __init__(self, name, parent):
        super(Function, self).__init__(name=name, parent=parent)
        self.name = name
        self.parent = parent


class Predicate(Function):
    def __init__(self, name, parent):
        super(Predicate, self).__init__(name=name, parent=parent)
        self.name = name
        self.parent = parent


class Expression(Step):
    def __init__(self, name, parent, humanId=None):
        super(Expression, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class BooleanExpression(Expression):
    """
    An BooleanExpression is a Boolean-valued Expression whose type is a Predicate. It represents
    a logical condition resulting from the evaluation of the Predicate. A BooleanExpression must
    subset, directly or indirectly, the Expression booleanEvaluations from the Base model
    library, which is typed by the base Predicate BooleanEvaluation. As a result,
    a BooleanExpression must always be typed by BooleanEvaluation or a subclass of
    BooleanEvaluation.

    Attributes
        /predicate : Predicate {redefines function}
        The Predicate that types the Expression.
    """

    def __init__(self, name, parent, humanId=None, predicate=None):
        super(BooleanExpression, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId

        self.predicate = predicate


class Invariant(BooleanExpression):
    def __init__(self, name, parent, humanId=None):
        super(Invariant, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class ReturnParameterMembership(ParameterMembership):
    def __init__(self, name, parent):
        super(ReturnParameterMembership, self).__init__(name=name, parent=parent)
        self.name = name
        self.parent = parent


class ResultExpressionMembership(FeatureMember):
    def __init__(self, name, parent):
        super(ResultExpressionMembership, self).__init__(name=name, parent=parent)
        self.name = name
        self.parent = parent


class FeatureReferenceExpression(Expression):
    def __init__(self, name, parent, humanId=None):
        super(FeatureReferenceExpression, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class InvocationExpression(Expression):
    def __init__(self, name, parent, humanId=None):
        super(InvocationExpression, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class LiteralExpression(Expression):
    def __init__(self, name, parent, humanId=None):
        super(LiteralExpression, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class LiteralInteger(LiteralExpression):
    def __init__(self, name, parent, humanId=None):
        super(LiteralInteger, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class LiteralRational(LiteralExpression):
    def __init__(self, name, parent, humanId=None):
        super(LiteralRational, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class LiteralBoolean(LiteralExpression):
    def __init__(self, name, parent, humanId=None):
        super(LiteralBoolean, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class LiteralString(LiteralExpression):
    def __init__(self, name, parent, humanId=None):
        super(LiteralString, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class LiteralInfinity(LiteralExpression):
    def __init__(self, name, parent, humanId=None):
        super(LiteralInfinity, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class NullExpression(Expression):
    def __init__(self, name, parent, humanId=None):
        super(NullExpression, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class OperatorExpression(InvocationExpression):
    def __init__(self, name, parent, humanId=None):
        super(OperatorExpression, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class FeatureChainExpression(OperatorExpression):
    def __init__(self, name, parent, humanId=None):
        super(FeatureChainExpression, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class CollectExpression(OperatorExpression):
    def __init__(self, name, parent, humanId=None):
        super(CollectExpression, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class SelectExpression(OperatorExpression):
    def __init__(self, name, parent, humanId=None):
        super(SelectExpression, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class Interaction(Behavior, Association):
    def __init__(self, name, parent, humanId=None):
        super(Interaction, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class ItemFlow(Step, Connector):
    def __init__(self, name, parent, humanId=None):
        super(ItemFlow, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class SuccessionItemFlow(ItemFlow, Succession):
    def __init__(self, name, parent, humanId=None):
        super(SuccessionItemFlow, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class FeatureValue(Membership):
    def __init__(self, name, parent):
        super(FeatureValue, self).__init__(name=name, parent=parent)
        self.name = name
        self.parent = parent


class MultiplicityRange(Multiplicity):
    def __init__(self, name, parent, humanId=None):
        super(MultiplicityRange, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class AnnotatingFeature(AnnotatingElement, Feature):
    def __init__(self, name, parent, humanId=None):
        super(AnnotatingFeature, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class MetadataFeature(Feature):
    def __init__(self, name, parent, humanId=None):
        super(MetadataFeature, self).__init__(name=name, parent=parent, humanId=humanId)
        self.name = name
        self.parent = parent
        self.humanId = humanId


class MetadataFeatureValue(FeatureValue):
    def __init__(self, name, parent):
        super(MetadataFeatureValue, self).__init__(name=name, parent=parent)
        self.name = name
        self.parent = parent


class Package(Namespace):
    """
    A Namespace is an Element that contains other Elements, known as its members, via Membership
    Relationships with those Elements. The members of a Namespace may be owned by the Namespace,
    aliased in the Namespace, or imported into the Namespace via Import Relationships with other
    Namespaces.

    A Namespace can provide names for its members via the memberNames specified by the Memberships
    in the Namespace. If a Membership specifies a memberName, then that is the name of the corresponding
    memberElement relative to the Namespace. Note that the same Element may be the memberElement
    of multiple Memberships in a Namespace (though it may be owned at most once), each of which
    may define a separate alias for the Element relative to the Namespace.

    Attributes
        importedMembership : Membership [0..*] {subsets membership, ordered}
            [Derived] The Memberships in this Namespace that result from Import Relationships between the
            Namespace and other Namespaces.
        member : Element [0..*] {ordered}
            [Derived] The set of all member Elements of this Namespace, derived as the memberElements of
            all memberships of the Namespace.
        membership : Membership [0..*] {ordered, union}
            [Derived] All Memberships in this Namespace, defined as the union of ownedMemberships and
            importedMemberships.
        ownedImport : Import [0..*] {subsets sourceRelationship, ownedRelationship, ordered}
            [Derived] The ownedRelationships of this Namespace that are Imports, for which the Namespace is
            the importOwningNamespace.
        ownedMember : Element [0..*] {subsets member, ordered}
            [Derived] The owned members of this Namespace, derived as the ownedMemberElements of the
            ownedMemberships of the Namespace.
        ownedMembership : Membership [0..*] {subsets membership, sourceRelationship, ownedRelationship, ordered}
            [Derived] The ownedRelationships of this Namespace that are Memberships, for which the Namespace is
            the membershipOwningNamespace.
    """

    def __init__(self, name, parent, humanId=None, importedMembership=None, member=None,
                 membership=None,
                 ownedImport=None, ownedMember=None, ownedMembership=None, ownedRelationship=None):
        super(Package, self).__init__(name=name, parent=parent, humanId=humanId,
                                      ownedRelationship=ownedRelationship)
        self.name = name
        self.parent = parent
        self.humanId = humanId
        self.importedMembership: [Membership] = importedMembership
        self.member: [Element] = member
        self.membership: [Membership] = membership
        self.ownedImport: [Import] = ownedImport
        self.ownedMember: [Element] = ownedMember
        self.ownedMembership: [Membership] = ownedMembership

    def importedMemberships(self, excluded):
        """
        Derive the imported Memberships of this Namespace as the importedMembership of all ownedImports,
        excluding those Imports whose importOwningNamespace is in the excluded set, and excluding
        Memberships that have distinguishability collisions with each other or with any ownedMembership.

        body:
            ownedImport->excluding(excluded->contains(importOwningNamespace)).importedMembership(excluded)
        """
        # set(self.ownedImport).difference()
        # importOwningNamespace in excluded
        return Membership

    def namesOf(self, element: Element):
        """
        Parameters
            element (Element): The Element in which we want to get the name of if it is known in this Namespace
        Returns
            [str]: The names of the given element as it is known in this Namespace.
        """
        return [n.name for n in self.member if element.name == n.name]


class ElementFilterMembership(Membership):
    def __init__(self, name, parent):
        super(ElementFilterMembership, self).__init__(name=name, parent=parent)
        self.name = name
        self.parent = parent
