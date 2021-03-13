begin
  var i: integer := 0;
  var b: integer := 1;
  try
    b := b div i;
  except
    on System.DivideByZeroException do
      writeln('divison error!!!');
  end;
  writeln('end process!!!');
end.