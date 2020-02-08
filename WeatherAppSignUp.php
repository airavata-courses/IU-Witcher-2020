<?php
if (isset($_GET['uname'])  and isset($_GET['password'])){
    $userId=$_GET['uname']; 
    $Password=$_GET['password'];

     $db = mysqli_connect("localhost", "root", "", "weatherappusers");
     $sql = "INSERT INTO userlogin VALUES ('$userId','$Password')";
     if(mysqli_query($db, $sql))
        {
            echo "User Created Successfully";
        }
    else{
            echo "Error";
    }


} else {
   echo "Not set";
}
?>