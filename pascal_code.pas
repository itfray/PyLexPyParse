begin
  cc.x := 2;
  cc.y := 3;
  cc.f(10);
  p := cc.f;
  cc.a.a := 12;
  
  rr := cc.aa();
  cc.aa()^.aa()^.a.a := -100;
end.