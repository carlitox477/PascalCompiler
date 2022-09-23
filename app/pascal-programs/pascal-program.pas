program numerosConsecutivos;
var numero, i: integer; pepito: boolean;

function agregarUno: integer;
   var numero, i: integer;
   begin
      agregarUno := 1;
   end;

function agregarUno(num: integer):integer;
   begin
      agregarUno := num +1;
   end;
   
procedure agregarUno(num: integer);
   var numero, i: integer;
   begin
      numero:=1;
   end;
   
function agregarUno(num: integer; bol: boolean): boolean;
   
   begin
        agregarUno := true;
   end;
   
procedure agregarUno(bol: boolean; num: integer; agregarUno: boolean);
   var numero, i: integer;
   begin
      numero:=1;
   end;

procedure imprimirCabecera(num: integer);
   begin
      write(num);
   end;

begin
   read(numero);

   imprimirCabecera(numero);

   i:= 1;
   while i< 19 do
      begin
         write(numero+i);
         i:= agregarUno(i);
      end;
   write(numero+20);
end.
