<?php
$host='db';
$user='devuser';
$password='devpass';
$db='test_db';

$conn = mysqli_connect($host, $user, $password, $db);

// if($conn){
// 	echo "connection established";
// }

$sql="CREATE TABLE IF NOT EXISTS userlogin (
  userId varchar(25) NOT NULL,
  Password varchar(100) NOT NULL,
  PRIMARY KEY (userId)
)";

$res=mysqli_query($conn, $sql);

// if($res){
// 	echo "table Created";
// }

// $sql = "SELECT * FROM userlogin";
// $result = $conn->query($sql);

// if ($result->num_rows > 0) {
//     // output data of each row
//     while($row = $result->fetch_assoc()) {
//         echo "id: " . $row["userId"]. " - Name: " . $row["Password"]. "<br>";
//     }
// } else {
//     echo "0 results";
// }


if ($_SERVER['REQUEST_METHOD'] === 'POST') {

$userId=$_POST['uname'];
$Password=$_POST['password'];

$sql = "INSERT INTO userlogin VALUES ('$userId','$Password')";
if(mysqli_query($conn, $sql))
        {
            echo "User Created Successfully";
        }
    else{
            echo mysqli_error($conn);
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

