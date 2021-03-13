begin
  var a: array[0..9] of integer;
  for var i := 0 to 9 do
    a[i] := i + 1;
  var s: integer := 0;
  foreach var val in a do
    s += val;
  var b: integer := 0;
  case 1 of
    1..2: b := 1;;
    3..4: b := 2;
  end;
end.