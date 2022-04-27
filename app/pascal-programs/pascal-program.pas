program numerosConsecutivos;
var numero, i: integer;

function agregarUno(num: integer):integer;
   begin
      agregarUno := num +1
   end;

procedure imprimirCabecera(num);
   begin
      write(num);
   end;

begin
   read(numero);

   imprimirCabecera(numero)

   i:= 1;
   while i< 19 do
      begin
         write(numero+i)
         i:= agregarUno(i);
      end;
   write(numero+20)
end.
