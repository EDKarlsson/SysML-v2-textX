try:
    from core_layer import Classifier, Feature, Multiplicity, FeatureMember
    from root_layer import Element, Namespace, Relationship, Membership, Import, AnnotatingElement
except:
    from kerml.classes.core_layer import Classifier, Feature, Multiplicity, FeatureMember
    from kerml.classes.root_layer import Element, Namespace, Relationship, Membership, Import, AnnotatingElement


class Class(Classifier):
    def __init__(self, name, parent):
        super(Class, self).__init__(name=name, parent=parent)


class DataType(Classifier):
    def __init__(self, name, parent):
        super(DataType, self).__init__(name=name, parent=parent)


class Structure(Class):
    def __init__(self, name, parent):
        super(Structure, self).__init__(name=name, parent=parent)


class Association(Classifier, Relationship):
    def __init__(self, name, parent, humanId=None):
        super(Association, self).__init__(name=name, parent=parent, humanId=humanId)


class AssociationStructure(Association, Structure):
    def __init__(self, name, parent, humanId=None):
        super(AssociationStructure, self).__init__(name=name, parent=parent, humanId=humanId)


class Connector(Feature, Relationship):
    def __init__(self, name, parent, humanId=None):
        super(Connector, self).__init__(name=name, parent=parent, humanId=humanId)


class BindingConnector(Connector):
    def __init__(self, name, parent, humanId=None):
        super(BindingConnector, self).__init__(name=name, parent=parent, humanId=humanId)


class Succession(Connector):
    def __init__(self, name, parent, humanId=None):
        super(Succession, self).__init__(name=name, parent=parent, humanId=humanId)


class Behavior(Class):
    def __init__(self, name, parent):
        super(Behavior, self).__init__(name=name, parent=parent)


class Step(Feature):
    def __init__(self, name, parent, humanId=None):
        super(Step, self).__init__(name=name, parent=parent, humanId=humanId)


class ParameterMembership(FeatureMember):
    def __init__(self, name, parent):
        super(ParameterMembership, self).__init__(name=name, parent=parent)


class Function(Behavior):
    def __init__(self, name, parent):
        super(Function, self).__init__(name=name, parent=parent)


class Predicate(Function):
    def __init__(self, name, parent):
        super(Predicate, self).__init__(name=name, parent=parent)


class Expression(Step):
    def __init__(self, name, parent, humanId=None):
        super(Expression, self).__init__(name=name, parent=parent, humanId=humanId)


class BooleanExpression(Expression):
    def __init__(self, name, parent, humanId=None):
        super(BooleanExpression, self).__init__(name=name, parent=parent, humanId=humanId)


class Invariant(BooleanExpression):
    def __init__(self, name, parent, humanId=None):
        super(Invariant, self).__init__(name=name, parent=parent, humanId=humanId)


class ReturnParameterMembership(ParameterMembership):
    def __init__(self, name, parent):
        super(ReturnParameterMembership, self).__init__(name=name, parent=parent)


class ResultExpressionMembership(FeatureMember):
    def __init__(self, name, parent):
        super(ResultExpressionMembership, self).__init__(name=name, parent=parent)


class FeatureReferenceExpression(Expression):
    def __init__(self, name, parent, humanId=None):
        super(FeatureReferenceExpression, self).__init__(name=name, parent=parent, humanId=humanId)


class InvocationExpression(Expression):
    def __init__(self, name, parent, humanId=None):
        super(InvocationExpression, self).__init__(name=name, parent=parent, humanId=humanId)


class LiteralExpression(Expression):
    def __init__(self, name, parent, humanId=None):
        super(LiteralExpression, self).__init__(name=name, parent=parent, humanId=humanId)


class LiteralInteger(LiteralExpression):
    def __init__(self, name, parent, humanId=None):
        super(LiteralInteger, self).__init__(name=name, parent=parent, humanId=humanId)


class LiteralRational(LiteralExpression):
    def __init__(self, name, parent, humanId=None):
        super(LiteralRational, self).__init__(name=name, parent=parent, humanId=humanId)


class LiteralBoolean(LiteralExpression):
    def __init__(self, name, parent, humanId=None):
        super(LiteralBoolean, self).__init__(name=name, parent=parent, humanId=humanId)


class LiteralString(LiteralExpression):
    def __init__(self, name, parent, humanId=None):
        super(LiteralString, self).__init__(name=name, parent=parent, humanId=humanId)


class LiteralInfinity(LiteralExpression):
    def __init__(self, name, parent, humanId=None):
        super(LiteralInfinity, self).__init__(name=name, parent=parent, humanId=humanId)


class NullExpression(Expression):
    def __init__(self, name, parent, humanId=None):
        super(NullExpression, self).__init__(name=name, parent=parent, humanId=humanId)


class OperatorExpression(InvocationExpression):
    def __init__(self, name, parent, humanId=None):
        super(OperatorExpression, self).__init__(name=name, parent=parent, humanId=humanId)


class FeatureChainExpression(OperatorExpression):
    def __init__(self, name, parent, humanId=None):
        super(FeatureChainExpression, self).__init__(name=name, parent=parent, humanId=humanId)


class CollectExpression(OperatorExpression):
    def __init__(self, name, parent, humanId=None):
        super(CollectExpression, self).__init__(name=name, parent=parent, humanId=humanId)


class SelectExpression(OperatorExpression):
    def __init__(self, name, parent, humanId=None):
        super(SelectExpression, self).__init__(name=name, parent=parent, humanId=humanId)


class Interaction(Behavior, Association):
    def __init__(self, name, parent, humanId=None):
        super(Interaction, self).__init__(name=name, parent=parent, humanId=humanId)


class ItemFlow(Step, Connector):
    def __init__(self, name, parent, humanId=None):
        super(ItemFlow, self).__init__(name=name, parent=parent, humanId=humanId)


class SuccessionItemFlow(ItemFlow, Succession):
    def __init__(self, name, parent, humanId=None):
        super(SuccessionItemFlow, self).__init__(name=name, parent=parent, humanId=humanId)


class FeatureValue(Membership):
    def __init__(self, name, parent):
        super(FeatureValue, self).__init__(name=name, parent=parent)


class MultiplicityRange(Multiplicity):
    def __init__(self, name, parent, humanId=None):
        super(MultiplicityRange, self).__init__(name=name, parent=parent, humanId=humanId)


class AnnotatingFeature(AnnotatingElement, Feature):
    def __init__(self, name, parent, humanId=None):
        super(AnnotatingFeature, self).__init__(name=name, parent=parent, humanId=humanId)


class MetadataFeature(Feature):
    def __init__(self, name, parent, humanId=None):
        super(MetadataFeature, self).__init__(name=name, parent=parent, humanId=humanId)


class MetadataFeatureValue(FeatureValue):
    def __init__(self, name, parent):
        super(MetadataFeatureValue, self).__init__(name=name, parent=parent)


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

    Attributes:
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

        @param excluded: Namespace
        @return membership:Membership
        """
        # set(self.ownedImport).difference()
        # importOwningNamespace in excluded
        return Membership

    def namesOf(self, element: Element) -> [str]:
        """
        Return the names of the given element as it is known in this Namespace.
        """
        return [n.name for n in self.member if element.name == n.name]


class ElementFilterMembership(Membership):
    def __init__(self, name, parent):
        super(ElementFilterMembership, self).__init__(name=name, parent=parent)
