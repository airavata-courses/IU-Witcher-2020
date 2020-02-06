<?php
echo "weather app";
if (isset($_GET['uname'])  and isset($_GET['password'])){
    $uname=$_GET['uname']; 
    $password=$_GET['password'];

    if(!strcmp($uname,"vishal") and !strcmp($password,"patel"))
    {
    	echo "True";
    }
    else{
    	echo "Invalid";
    }

} else {
   echo "Not set";
}
?>