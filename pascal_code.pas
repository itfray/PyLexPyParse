var
  a1 := 1;
  b1: integer = -3;
  c1: integer := 2;
  d1, e1, f1: real;
  (g1, h1) := (5, 999);
begin
  var a2 := 1;
  var b2: integer = -3;
  var c2: integer := 2;
  var d2, e2, f2: real;
  var (g2, h2) := (5, 999);
  (var i2, var j2) := (100, -100);
end.