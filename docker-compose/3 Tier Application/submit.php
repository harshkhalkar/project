<?php 
$name=$_POST["name"];
$email=$_POST["email"];
$website= $_POST["website"];
$comment=$_POST["comment"];
$gender=$_POST["gender"];

echo $name;
echo $email;
echo $gender;
echo $comment;
echo $website;
 
$servername = "db";
$username = "root";
$password = "";
$dbname = "info";
 
// Create connection
$conn = mysqli_connect($servername, $username, $password, $dbname);

// Check connection
if (!$conn) {
  die("Connection failed: " . mysqli_connect_error());
}

$sql = "INSERT INTO users (name,email,website,comment,gender)VALUES('$name','$email','$website','$comment','$gender')";

if (mysqli_query($conn, $sql)) {
  echo "New record created successfully";
} else {
  echo "Error: " . $sql . "<br>" . mysqli_error($conn);
}
mysqli_close($conn);
?>
