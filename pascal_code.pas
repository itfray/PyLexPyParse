type
  Person = class
    name: string;
    age: integer;
    procedure foo(); virtual;
    begin
      ;
    end;
    property PersonName: string read name write name; virtual;
  end;
begin
end.