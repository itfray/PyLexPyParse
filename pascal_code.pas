type
  Person = class
  public
    nm: string;
    age: integer;
    constructor (nm: string; age: integer);
    begin
      Self.nm := nm;
      Self.age := age;
    end;
  end;
begin
  var p1, p2, pres: Person;
  p1 := new Person('Mike', 12);
  p2 := new Person('Kendal', 100);
  writeln(pres);
end.