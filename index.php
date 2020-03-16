    <?php 
    function check_password($username, $password){
        $pwd_file = 'auth.txt';
        if(!$fh = fopen($pwd_file, "r")) {die("<p>Could not open password file");}
        $match = 0;
        $pwd = $password;
        while(!feof($fh)) {
          $line = fgets($fh, 4096);
          $user_pass = explode(":", $line);
      
          if($user_pass[0] == $username) {
            if(rtrim($user_pass[1]) == $pwd) {
              $match = 1;
              break;
            }
          }
          $match = 2; 
        }
        if($match == '1') {
           echo "True";
        } 
        if($match == '2') {
           echo "False";
        } 
        fclose($fh);
    }
    if ($_SERVER['REQUEST_METHOD'] === 'GET'){
        check_password($_GET['username'], $_GET['password']);
    }
    else{
      $myfile = fopen("auth.txt", "a") or die("Unable to open file!");
      $txt = $_POST['username'].':'.$_POST['password']."\n";
      echo "User Created Successfully";
      fwrite($myfile, $txt);
      fclose($myfile);
      }
      ?>