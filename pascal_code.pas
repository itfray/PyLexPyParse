type
  R = record
        public
          x,y: integer;
          constructor (x,y: integer);
          begin
            Self.x := x;
            Self.y := y;
          end;
          function foo(a: integer): integer := a + 1;
          function foo(a,b: integer): integer := a + b + 2;
      end;
var
  rr: R;
begin
end.