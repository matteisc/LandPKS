<?php
include_once 'LandPKS_Plots_Map_Supports.inc';

$username = "root";
$password ="";
$database = "apex";
// Opens a connection to a MySQL server
$connection =mysql_connect ('localhost', $username, $password);
if (!$connection) {
  die('Not connected : ' . mysql_error());
}

// Set the active MySQL database
$db_selected = mysql_select_db($database, $connection);
if (!$db_selected) {
  die ('Can\'t use db : ' . mysql_error());
}

// Select all the rows in the markers table
$query = "SELECT name,recorder_name,latitude,longitude FROM landpks_input_data WHERE boolean_test_plot = 0";
$result = mysql_query($query);
if (!$result) {
  die('Invalid query: ' . mysql_error());
}

mysql_close($connection);

header("Content-type: text/xml");

// Start XML file, echo parent node
echo '<plots>';

// Iterate through the rows, printing XML nodes for each
while ($row = @mysql_fetch_assoc($result)){
  // ADD TO XML DOCUMENT NODE
  echo '<plot ';
  echo 'name="' . parseToXML(parseName($row['name'])) . '" ';
  echo 'recorder_name="' . parseToXML($row['recorder_name']) . '" ';
  echo 'lat="' . $row['latitude'] . '" ';
  echo 'lng="' . $row['longitude'] . '" ';
  echo 'type="landinfo_plot"';
  echo '/>';
}

// End XML file
echo '</plots>';
?>

