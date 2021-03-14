var
  f: integer;
  procedure forall(a: array of real; f: real->real);
  begin
    for var i := 0 to a.Length-1 do
      a[i] := f(a[i]);
  end;
begin
end.