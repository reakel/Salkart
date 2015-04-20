<?php
error_reporting(E_ALL);
ini_set('display_errors','on');
//$rawmaskinliste=$_POST['list'];
//$maskinliste=json_encode($rawmaskinliste);
//echo $maskinliste;

$db=new PDO('sqlite:/usr/local/share/innloggingslogging/innlogging.db');
$stm=$db->prepare("SELECT * FROM maskiner");
$stm->execute();
$result=$stm->fetchAll(PDO::FETCH_ASSOC);
//var_dump($result);
$json=json_encode($result);
echo $json;

?>


