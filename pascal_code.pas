begin
  var i: integer := 0;
  var b: integer := 1;
  try
    b := b + i;
  except
    i += 1;
    i += 2;
  end;
end.