<!DOCTYPE html>
<html>
<body>

<?php
$txt = "PHP";

$salt = "-e36d8fbc-9482-4f00-96c6-ae5370d04e08";
$secret = "9be4a60f645f" . $salt;

$password = "9be4a60f645f-e36d8fbc-9482-4f00-96c6-ae5370d04e09";

$h1 = hash('fnv164', $password);
$h2 = hash('fnv164', $secret);

echo $h1;
echo "\n";
echo $h2;
echo "\n";

if ($h2 == $h1) {
	echo "mamene";
}
?>

</body>
</html>
