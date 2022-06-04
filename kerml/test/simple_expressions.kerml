package Expressions {
    x = 1;

//	b = x > y? x-y: y-x;
//	c = x->collect {in xx; xx + 1};
//	c1 = x.{in xx; xx + 1};
//	d = x->select {in xx; xx != null};
//	d1 = x.?{in xx; xx != null};
//	e = x->reduce {in s; in t; s + t}->reduce '+';
//
//	xx = x == 1 && y == 2? a:
//	     x == 2? b:
//	     x == 3? c:
//	     0;
//
//	yy = if x == 1 and y == 2? a
//	     else if x == 2? b
//	     else if x == 3? c
//	     else 0;
//
//    function TotalMass(partMass, subparts) {
//		partMass + (subparts->collect {in p; totalMass(partMass, subparts)}->reduce '+' ?? 0.0)
//	}
//
//	expr totalMass: TotalMass (mass, sub);
//
//	feature f {
//		expr s(x) : Boolean;
//	}
//
//	bb : Boolean = f.s(1);
//
//	class C {
//		count := 0;
//	}
}