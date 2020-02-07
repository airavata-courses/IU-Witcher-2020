<?php
echo "weather app";
if (isset($_GET['uname'])  and isset($_GET['password'])){
    $uname=$_GET['uname']; 
    $password=$_GET['password'];

    

} else {
   echo "Not set";
}
?>