from root_layer import Element, Namespace, Relationship, Membership, Import
import json


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

    def __init__(self, name, parent, humanId=None, ownedRelationship=None,
                 importedMembership=None, member=None, membership=None,
                 ownedImport=None, ownedMember=None, ownedMembership=None):
        super(Package, self).__init__(name=name, parent=parent, humanId=humanId, ownedRelationship=ownedRelationship)
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

