<?php
if (isset($_GET['uname'])  and isset($_GET['password'])){
    $userId=$_GET['uname']; 
    $Password=$_GET['password'];
    
    $db = mysqli_connect("localhost", "root", "", "weatherappusers");
    $sql="SELECT * FROM userlogin WHERE userId='$userId' and Password='$Password'";

 
	if ($res = mysqli_query($db, $sql)) { 
    
    	if (mysqli_num_rows($res) > 0) { 
			echo "True";
			}
		else{
			echo "False";
		}	

		}

} else {
   echo "Not set";
}
?>