<?php
$host="localhost:3308";
$user="Hadi";
$pass="Douda.@12345";
$dbc = mysqli_connect("$host","$user","$pass");
if(!$dbc){
die("NOT CONNECTED:" . mysqli_error());
}
//select database
$db_select =mysqli_select_db($dbc, "employee");
if(!$db_select){
die("cant connect :" . mysqli_error());
}

?>
 

 