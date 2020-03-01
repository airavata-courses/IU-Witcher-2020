<!-- ./php/index.php -->

<html>
    <head>
        <title>Hello World</title>
    </head>

    <body>
        <?php
		if (isset($_GET['uname'])  and isset($_GET['password'])){
		$userId=$_GET['uname'];
		$Password=$_GET['password'];
		if($userId=="vishal"){
			if($Password=="12345")
			{
				echo "True";
			}else{
			echo "False";
			}
		}

		}
		else{
			echo "Credentials Missing";
		}
		?>
		
    </body>
</html>