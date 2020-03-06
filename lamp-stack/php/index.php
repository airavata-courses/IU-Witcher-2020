<?php
$host='db';
$user='devuser';
$password='devpass';
$db='test_db';

$conn = mysqli_connect($host, $user, $password, $db);


$sql="CREATE TABLE IF NOT EXISTS userlogin (
  userId varchar(25) NOT NULL,
  Password varchar(100) NOT NULL,
  PRIMARY KEY (userId)
)";

$res=mysqli_query($conn, $sql);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

$userId=$_POST['uname'];
$Password=$_POST['password'];

$sql = "INSERT INTO userlogin VALUES ('$userId','$Password')";
if(mysqli_query($conn, $sql))
        {
            echo "User Created Successfully";
        }
    else{
            echo "Error";
    	}
}

else{	
	    $userId=$_GET['uname'];
		$Password=$_GET['password'];
		if($userId=="guest" and $Password=="guest"){
			echo "True";
			}
		else{		
    		$sql="SELECT * FROM userlogin WHERE userId='$userId' and Password='$Password'";
			if ($res = mysqli_query($conn, $sql)) { 
		    	if (mysqli_num_rows($res) > 0) { 
					echo "True";
					}
				else{
					echo "False";
				}	
				}
			}
}
?>

