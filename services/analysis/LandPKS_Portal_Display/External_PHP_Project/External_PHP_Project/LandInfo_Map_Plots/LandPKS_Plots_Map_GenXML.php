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
$query = "SELECT * FROM landpks_input_data WHERE boolean_test_plot = 0";
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
  echo 'slope="' . $row['slope'] . '" ';
  echo 'slope_shape="' . $row['slope_shape'] . '" ';
  echo 'land_cover="' . $row['land_cover'] . '" ';
  if ($row['boolean_grazed'] == 1) {
    echo 'grazed= "Yes" ';
} else {
    echo 'grazed= "No" ';
}

  if ($row['boolean_flooding'] == 1) {
    echo 'flooding= "Yes" ';
} else {
    echo 'flooding= "No" ';
}

  if ($row['boolean_surface_cracking'] == 1) {
    echo 'surface_cracking= "Yes" ';
} else {
    echo 'surface_cracking= "No" ';
}
  if ($row['boolean_surface_salt'] == 1) {
    echo 'surface_salt= "Yes" ';
} else {
    echo 'surface_salt= "No" ';
}
  echo 'texture_for_soil_horizon_1="' . $row['texture_for_soil_horizon_1'] . '" ';
  echo 'texture_for_soil_horizon_2="' . $row['texture_for_soil_horizon_2'] . '" ';
  echo 'texture_for_soil_horizon_3="' . $row['texture_for_soil_horizon_3'] . '" ';
  echo 'texture_for_soil_horizon_4="' . $row['texture_for_soil_horizon_4'] . '" ';
  echo 'texture_for_soil_horizon_5="' . $row['texture_for_soil_horizon_5'] . '" ';
  echo 'texture_for_soil_horizon_6="' . $row['texture_for_soil_horizon_6'] . '" ';
  echo 'texture_for_soil_horizon_7="' . $row['texture_for_soil_horizon_7'] . '" ';			
  
  echo 'rock_fragment_for_soil_horizon_1="' . $row['rock_fragment_for_soil_horizon_1'] . '" ';  			
  echo 'rock_fragment_for_soil_horizon_2="' . $row['rock_fragment_for_soil_horizon_2'] . '" ';			
  echo 'rock_fragment_for_soil_horizon_3="' . $row['rock_fragment_for_soil_horizon_3'] . '" ';			
  echo 'rock_fragment_for_soil_horizon_4="' . $row['rock_fragment_for_soil_horizon_4'] . '" ';			
  echo 'rock_fragment_for_soil_horizon_5="' . $row['rock_fragment_for_soil_horizon_5'] . '" ';			
  echo 'rock_fragment_for_soil_horizon_6="' . $row['rock_fragment_for_soil_horizon_6'] . '" ';			
  echo 'rock_fragment_for_soil_horizon_7="' . $row['rock_fragment_for_soil_horizon_7'] . '" ';
	
  echo 'type="landinfo_plot"';
  echo '/>';
}

// End XML file
echo '</plots>';
?>

