namespace Types {
    element Base;
    abstract type O specializes Base;
    type A specializes O;
    type B specializes O;
    type Original specializes A;
    conjugation c1 conjugate A conjugates Original;
	conjugation c2 conjugate B ~ Original;
}