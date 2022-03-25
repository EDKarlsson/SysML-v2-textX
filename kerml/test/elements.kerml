namespace root {
    // Test Single Line Note
    element <e145>;

    element <'1.2.4'> MyName;

    element A;
    element C;

    element B {
        relationship <x> {
            element <y>;
            relationship from B to A;
        }
        relationship to C;
    }
    // fmdosag
    element X {
        doc <X_comment>
            /* This is a documentation comment about X. */
        relationship to B;
    }
}