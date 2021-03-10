begin
  var a: array[0..9] of integer;
  for var i := 0 to 9 do
    a[i] := i + 1;
  var s: integer := 0;
  foreach var val in a do
    s += val;
end.