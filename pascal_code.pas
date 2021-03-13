label 1,2,3,4,5;
begin
  var i := 5;
2: if i<0 then goto 1;
  writeln(i);
  Dec(i);
  goto 2;
1: 2
4: 2
5:
end.