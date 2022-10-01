program numerosConsecutivos;
var numero, i: integer; pepito: boolean;
   
   
function agregarUno(num: integer; bol: boolean): integer;
   begin
        agregarUno := num;
   end;

begin
   read(numero , pepito);

   i:= 1;
   while i< 19 do
      begin
         write(numero+i);
         i:= agregarUno(i,pepito);
      end;
   write(numero+20);
end.
