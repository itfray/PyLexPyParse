begin
  var i: integer := 0;
  var b: integer := 1;
  try
    b := b div i;
  except
    on integer do
      i := -1;
    on a: integer do
      i := 1;
    else
      i += 3;
  end;
end.