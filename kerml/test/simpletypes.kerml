namespace Types {
    abstract type A specializes Something;
    type all x specializes A, Something;

    type Super specializes Something {
        private package P {
            type Sub specializes Super;
        }
    }
}