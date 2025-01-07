var $phoneNumber : Text
var $message : Text

ARRAY TEXT($Nomi; 0)
APPEND TO ARRAY($Nomi; "Marco")
APPEND TO ARRAY($Nomi; "Giordano")

ARRAY TEXT($Prodotti; 0)
APPEND TO ARRAY($Prodotti; "Taglia erba")
APPEND TO ARRAY($Prodotti; "Saldatrice")
C_TEXT($ProdottoOprodotti)
If (Size of array($Prodotti)>1)
	$ProdottoOprodotti:=" I tuoi prodotti sono pronti "
Else 
	$ProdottoOprodotti:=" Il tuo prodotto è pronto "
End if 
Productlist:=New list
ARRAY TO LIST($Prodotti; Productlist)

$phoneNumber:="+3(937564)97700"
$message:="Caro "+$Nomi{1}+$ProdottoOprodotti+"per il ritiro presso la nostra sede"


// Python script path
var $pythonScriptPath : Text
$pythonScriptPath:="/Users/magazzino_lol_gen_2/Documents/seleniumwapp/read_variable.py"

// Construct the command with phone number and message as arguments
var $command : Text
$command:="/Users/magazzino_lol_gen_2/Documents/seleniumwapp/.venv/bin/python3 "+Char(34)+$pythonScriptPath+Char(34)+" "+Char(34)+$phoneNumber+Char(34)+" "+Char(34)+$message+Char(34)

// Execute the Python script using SystemWorker
var $sw : 4D.SystemWorker
$sw:=4D.SystemWorker.new($command)

// Wait for the script to complete
$sw.wait()
// response from Python (output of the script<all print() in py>)
var $response : Text
$response:=$sw.response
$responseError:=$sw.responseError

If ($responseError="")
	ALERT("senza errori")
Else 
	ALERT("con errori")
	
End if 
If ($response="OK\n")
	ALERT("print ok in py")
End if 

