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

    def __init__(self, name, parent, humanId=None, target=None, source=None,
                 ownedRelatedElement=None, owningRelatedElement=None):
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

        self.owningRelatedElement = owningRelatedElement


class AnnotatingElement(Element):
    """
    An AnnotatingElement is an Element that provides additional description of or metadata on some other Element.
    An AnnotatingElement is attached to its annotatedElement by an Annotation Relationship.
    Attributes:
        annotatedElement : Element [0..*] {ordered}
            [Derived] The Elements that are annotated by this AnnotatingElement,
            derived as the annotatedElements of the annotations of this AnnotatingElement.
        annotation : Annotation [0..*] {subsets sourceRelationship, ordered}
            The Annotations that relate this AnnotatingElement to its annotatedElements.
    """

    def __init__(self, name, parent, annotatedElement=None, annotation=None):
        super(AnnotatingElement, self).__init__(name=name, parent=parent)
        self.annotatedElement: Element = annotatedElement
        self.annotation: Annotation = annotation


class Annotation(Relationship):
    """
    An Annotation is a Relationship between an AnnotatingElement
    and the Element that is annotated by that AnnotatingElement.
    Attributes:
        annotatedElement : Element {redefines target}
            The Element that is annotated by the annotatingElement of this Annotation.
        annotatingElement : AnnotatingElement {redefines source}
            The AnnotatingElement that annotates the annotatedElement of this Annotation.
        owningAnnotatedElement : Element [0..1] {subsets annotatedElement, redefines owningRelatedElement}
            The annotatedElement of this Annotation, when it is also its owningRelatedElement.
    """

    def __init__(self, name, parent, annotatedElement=None, annotatingElement=None, owningAnnotatedElement=None):
        super(Annotation, self).__init__(name=name, parent=parent)
        self.annotatedElement: Element = annotatedElement
        self.annotatingElement: AnnotatingElement = annotatingElement
        self.owningAnnotatedElement: Element = owningAnnotatedElement


class ModelComment(AnnotatingElement):
    """
    A Comment is AnnotatingElement whose body in some way describes its annotatedElements.
    Attributes:
        body : String
            The annotation text for the Comment.
    """

    def __init__(self, parent, name='', body=''):
        super(ModelComment, self).__init__(name=name, parent=parent)
        self.body = body


class Documentation(Annotation):
    """
    Documentation is an Annotation whose annotatingElement is a Comment that provides documentation
    of the annotatedElement. Documentation is always an ownedRelationship of its annotedElement.

    Attributes:
        documentingComment : Comment {subsets ownedRelatedElement, redefines annotatingElement}
            The Comment, which is owned by the Documentation Relationship, that documents the
            owningDocumentedElement of this Documentation.
        owningDocumentedElement : Element {redefines owningAnnotatedElement}
            The annotatedElement of this Documentation, which must own the Relationship.
    """

    def __init__(self, parent, name='', documentingComment=None, owningDocumentedElement=None):
        super(Documentation, self).__init__(name=name, parent=parent)
        self.documentingComment = documentingComment
        self.owningDocumentedElement = owningDocumentedElement


class OwnedDocumentation(Documentation):
    def __init__(self, parent, documentingComment, name=''):
        super(OwnedDocumentation, self).__init__(name=name, parent=parent)
        self.documentingComment = documentingComment


class TextualRepresentation(AnnotatingElement):
    """
    A TextualRepresentation is an AnnotatingElement that whose body represents the
    representedElement in a given language. The named language can be a natural language,
    in which case the body is an informal representation, or an artificial language,
    in which case the body is expected to be a formal, machine-parsable representation.

    Attributes:
        body : String
            A textual representation of the representedElement in the given language.
        language : String
            The natural or artificial language in which the body text is written.
        representedElement : Element {redefines annotatedElement}
            [Derived] The Element represented textually by this TextualRepresentation,
            which is its single annotatedElement.
    """

    def __init__(self, parent, name='', body='', language='', representedElement=None):
        super(TextualRepresentation, self).__init__(name=name, parent=parent)
        self.language = language
        self.body = body
        self.representedElement = representedElement


class Import(Relationship):
    """
    An Import is a Relationship between an importOwningNamespace in which one or more of the visible
    Memberships of the importedNamespace become importedMemberships of the importOwningNamespace.
    If isImportAll = false (the default), then only public Memberships are considered "visible".
    If isImportAll = true, then all Memberships are considered "visible", regardless of their
    declared visibility.

    If no importedMemberName is given, then all visible Memberships are imported from the
    importedNamespace. If isRecursive = true, then visible Memberships are also recursively
    imported from all visible ownedMembers of the Namespace that are also Namespaces.

    If an importedMemberName is given, then the Membership whose effectiveMemberName is that
    name is imported from the importedNamespace, if it is visible. If isRecursive = true and
    the imported memberElement is a Namespace, then visible Memberships are also recursively
    imported from that Namespace and its owned sub-Namespaces.

    Attributes:
        importedMemberName : String [0..1]
            The effectiveMemberName of the Membership of the importedNamspace to be imported.
            If not given, all public Memberships of the importedNamespace are imported.
        importedNamespace : Namespace {redefines target}
            The Namespace whose visible members are imported by this Import.
        importOwningNamespace : Namespace {subsets owningRelatedElement, redefines source}
            [Derived] The Namespace into which members are imported by this Import, which must be the
            owningRelatedElement of the Import.
        isImportAll : Boolean
            Whether to import memberships without regard to declared visibility.
        isRecursive : Boolean
            Whether to recursively import Memberships from visible, owned sub-namespaces.
        visibility : VisibilityKind
            The visibility level of the imported members from this Import relative to the importOwningNamespace.
    """

    def __init__(self, name, parent, importedMemberName=None, importNamespace=None, importOwningNamespace=None):
        super(Import, self).__init__(name=name, parent=parent)
        self.importedMemberName: str = importedMemberName
        self.importedNamespace: Namespace = importNamespace
        self.importOwningNamespace: Namespace = importOwningNamespace
        self.isImportAll: bool = False
        self.isRecursive: bool = False
        self.visibility = None


class Namespace(Element):
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

    def __init__(self, name, parent, importedMembership=None, member=None,
                 membership=None, ownedImport=None, ownedMember=None, ownedMembership=None):
        super(Namespace, self).__init__(name=name, parent=parent)
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


class Membership(Relationship):
    """
    Membership is a Relationship between a Namespace and an Element that indicates the Element is
    a member of (i.e., is contained in) the Namespace. The Membership may define a memberName for
    the Element as a member of the Namespace and specifies whether or not the Element is publicly
    visible as a member of the Namespace from outside the Namespace. The Element may be owned by
    the Namespace via the Membership, in which case it is an ownedMember of the Namespace, or it
    may be referenced but not owned, in which the Membership provides an alias for the Element in
    the Namespace.

    Attributes:
        effectiveMemberName : String
            [Derived] If the memberName is empty, then the effectiveName of the memberElement.
            Otherwise, the same as the memberName.
        memberElement : Element {redefines target}
            The Element that becomes a member of the membershipOwningNamespace due to this Membership.
        memberName : String [0..1]
            The name of the memberElement in membershipOwningNamespace.
        membershipOwningNamespace : Namespace {subsets membershipNamespace, owningRelatedElement, redefines source}
            [Derived] The Namespace of which the memberElement becomes a member due to this Membership.
        ownedMemberElement : Element [0..1] {subsets memberElement, ownedRelatedElement}
            The memberElement of this Membership if it is owned by the Membership as an ownedRelatedElement.
        visibility : VisibilityKind
            Whether the Membership of the memberElement in the membershipOwningNamespace is publicly
            visible outside that Namespace.
    """

    def __init__(self, name, parent):
        super(Membership, self).__init__(name=name, parent=parent)
        self.effectiveMemberName = None
        self.memberElement = None
        self.memberName = None
        self.membershipOwningNamespace = None
        self.ownedMemberElement = None
        self.visibility = None

    def isDistinguishableFrom(self, other) -> bool:
        """Whether this Membership is distinguishable from a given other Membership. By default, this is true if the
        memberName of this Membership is either empty or is different the memberName of the other Membership,
        or if the metaclass of the memberElement of this Membership is different than the metaclass of the
        memberElement of the other Membership. But this may be overridden in specializations of Membership.

        @param other: Membership
        """

        return True
