<?php
/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $path
 * @param unknown_type $type
 */
function delete_file($path,$type){
  $files = glob(FOLDER_PATH_CSV_EXPORT."*.csv");
  foreach ($files as $file){
    if (is_file($file)){
      unlink($file);
    }
  }
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $user
 */
function isVisile($user){
  if ($user->uid == 4 && $user->name == "abeh"){
    return true;
  } else if ($user->uid == 5 && $user->name == "jbeniston"){
    return true;
  } else if ($user->uid == 19 && $user->name == "nasim_gh") {
    return true;
  } else if ($user->uid == 1){
    return true;
  } else {
    return false;
  }
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 */
function call_Python_Sync_RHM_Data($recorder_name, $last_access_date){
  $cmd = 'cd Python_APEX && cd 16_RHM_PROJECT_GET_DATA_API && python C:\xampp\htdocs\APEX\Python_APEX\16_RHM_PROJECT_GET_DATA_API\Run_main_RHM_Sync_Data.py -recorder_name ' . $recorder_name . ' -date ' . $last_access_date;
  $output = exec($cmd);
  echo $output;
  if ($output == "ERROR[100]:LOCATION_IS_NOT_SUPPORTED"){
    return -1;
  }
  return 1;
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $video_version_id
 */
function check_exit_RHM_record($name, $recorder_name){
  $result = db_query("SELECT 1 as rs FROM rhm_input_data WHERE name ='" . trim($name) ."' AND recorder_name = '" . trim($recorder_name) . "'");
  foreach ($result as $record){
    if ($record->rs == 1){
      return true;
    }
  }
  return false;
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $name
 */
function get_number_of_record_follow_by_name($name) {
  $result = db_query("SELECT COUNT(ID) as rs FROM rhm_input_data WHERE UCASE(name) ='" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
     return $record->rs;
  }
  return 0;
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $name
 */
function get_group_1_for_output_data_RHM_2($name) {
  $result = db_query("SELECT SUM(bare_total) as rs FROM rhm_input_data WHERE UCASE(name) = '" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
     $nBare_in_all = $record->rs;
  }
  $object->bare_ground_1_percent = 0;
  $object->bare_ground_1_percent = $nBare_in_all;
  $object->veg_cover_percent = 100 - $object->bare_ground_1_percent;
  return $object;
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $name
 */
function get_group_1_for_output_data_RHM($name) {
  /* Count bare in stick_segment_0 */
  $nBare_in_stick_0 = 0;
  $result = db_query("SELECT COUNT(ID) as rs FROM rhm_input_data WHERE UCASE(stick_segment_0) LIKE '%BARE%' AND UCASE(name) ='" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
     $nBare_in_stick_0 = $record->rs;
  }
  
  /* Count bare in stick_segment_1 */
  $nBare_in_stick_1 = 0;
  $result = db_query("SELECT COUNT(ID) as rs FROM rhm_input_data WHERE UCASE(stick_segment_1) LIKE '%BARE%' AND UCASE(name) ='" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
     $nBare_in_stick_1 = $record->rs;
  }
  
  /* Count bare in stick_segment_2 */
  $nBare_in_stick_2 = 0;
  $result = db_query("SELECT COUNT(ID) as rs FROM rhm_input_data WHERE UCASE(stick_segment_2) LIKE '%BARE%' AND UCASE(name) ='" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
     $nBare_in_stick_2 = $record->rs;
  }
  
  /* Count bare in stick_segment_0 */
  $nBare_in_stick_3 = 0;
  $result = db_query("SELECT COUNT(ID) as rs FROM rhm_input_data WHERE UCASE(stick_segment_3) LIKE '%BARE%' AND UCASE(name) ='" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
     $nBare_in_stick_3 = $record->rs;
  }
  
  /* Count bare in stick_segment_0 */
  $nBare_in_stick_4 = 0;
  $result = db_query("SELECT COUNT(ID) as rs FROM rhm_input_data WHERE UCASE(stick_segment_4) LIKE '%BARE%' AND UCASE(name) ='" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
     $nBare_in_stick_4 = $record->rs;
  }
  $object->bare_ground_1_percent = 0;
  $object->bare_ground_1_percent = $nBare_in_stick_0 + $nBare_in_stick_1 + $nBare_in_stick_2 + $nBare_in_stick_3 + $nBare_in_stick_4;
  $object->veg_cover_percent = 100 - $object->bare_ground_1_percent;
  return $object;
}
 

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $name
 */
function get_group_2_for_output_data_RHM($name) {
  $result = db_query("SELECT SUM(bare_total) as bare, SUM(perennial_grasses_total) as grass  ,SUM(trees_total) as trees, SUM(shrubs_total) as shrubs, SUM(sub_shrubs_total) as sub_shrubs, SUM(annuals_total) as annual, SUM(herb_litter_total) as herb_litter, SUM(wood_litter_total) as wood_litter, SUM(rock_total) as rock FROM rhm_input_data WHERE UCASE(name) ='" . trim($name) ."'");
  foreach ($result as $record){
    $objects->bare_ground_2 = (int)$record->bare;
    $objects->perennial_grasses = (int)$record->grass;
    $objects->tree = (int)$record->trees;
    $objects->shrubs = (int)$record->shrubs;
    $objects->sub_shrubs = (int)$record->sub_shrubs;
    $objects->annual = (int)$record->annual;
    $objects->herb_litter = (int)$record->herb_litter;
    $objects->wood_litter = (int)$record->wood_litter;
    $objects->rock = (int)$record->rock;

    return $objects;
  }
  return 0;
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $name
 */
function get_group_3_for_output_data_RHM($name,$total_records_by_name){
  //$total_records_by_name = get_number_of_record_follow_by_name($name);
  $result = db_query("SELECT COUNT(ID) as canopy_gap FROM rhm_input_data WHERE UCASE(canopy_gap) = 'TRUE' and UCASE(name) = '" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
    $count_true_canopy_gap = $record->canopy_gap;
    break;
  }
  //echo $count_true_canopy_gap . ":" . $total_records_by_name;
  $canopy_gap_percent = ((float) $count_true_canopy_gap / $total_records_by_name) *100;
  $object->canopy_gap_percent = (int)$canopy_gap_percent;
  
  $result = db_query("SELECT COUNT(ID) as basal_gap FROM rhm_input_data WHERE UCASE(basal_gap) = 'TRUE' and UCASE(name) = '" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
    $count_true_basal_gap = $record->basal_gap;
    break;
  }
  
  $basal_gap_percent = ((float) $count_true_basal_gap / $total_records_by_name) *100;
  $object->basal_gap_percent = (int)$basal_gap_percent;
  
  return $object;
}

function get_group_4_for_output_data_RHM($name,$total_records_by_name) {
  //$total_records_by_name = get_number_of_record_follow_by_name($name);
  $result = db_query("SELECT SUM(species_1_density) as species_1 FROM rhm_input_data WHERE UCASE(name) = '" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
    $species_1_sum = $record->species_1;
    break;
  }
  $species_1_density = (float) $species_1_sum / $total_records_by_name;
  $object->species_1_density_percent = $species_1_density;
  
  $result = db_query("SELECT SUM(species_2_density) as species_2 FROM rhm_input_data WHERE UCASE(name) = '" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
    $species_2_sum = $record->species_2;
    break;
  }
  $species_2_density = (float) $species_2_sum / $total_records_by_name;
  $object->species_2_density_percent = $species_2_density;
  
  return $object;
}

function get_group_5_for_output_data_RHM($name,$total_records_by_name){
  
  $result = db_query("SELECT COUNT(ID) as count_10cm FROM rhm_input_data WHERE UCASE(canopy_height) like '%<10cm%' AND UCASE(name) = '" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
    $count_10cm = $record->count_10cm;
    break;
  }
  $canopy_height_10cm = (float) ($count_10cm / $total_records_by_name) * 100;
  $object->canopy_height_smaller_10_cm = (int) $canopy_height_10cm;
  
  
  $result = db_query("SELECT COUNT(ID) as count_10_50cm FROM rhm_input_data WHERE UCASE(canopy_height) like '%10-50cm%' AND UCASE(name) = '" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
    $count_10_50cm = $record->count_10_50cm;
    break;
  }
  $canopy_height_10_50cm = (float) ($count_10_50cm / $total_records_by_name) * 100;
  $object->canopy_height_10_50_cm = (int) $canopy_height_10_50cm;
  
  $result = db_query("SELECT COUNT(ID) as count_50cm_1m FROM rhm_input_data WHERE UCASE(canopy_height) like '%50cm-1m%' AND UCASE(name) = '" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
    $count_50cm_1m = $record->count_50cm_1m;
    break;
  }
  $canopy_height_50cm_1m = (float) ($count_50cm_1m / $total_records_by_name) * 100;
  $object->canopy_height_50cm_1m = (int) $canopy_height_50cm_1m;
  
  
  $result = db_query("SELECT COUNT(ID) as count_1m_2m FROM rhm_input_data WHERE UCASE(canopy_height) like '%1-2m%' AND UCASE(name) = '" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
    $count_1m_2m = $record->count_1m_2m;
    break;
  }
  $canopy_height_1m_2m = (float) ($count_1m_2m / $total_records_by_name) * 100;
  $object->canopy_height_1m_2m = (int) $canopy_height_1m_2m;
  
  
  $result = db_query("SELECT COUNT(ID) as count_2m_3m FROM rhm_input_data WHERE UCASE(canopy_height) like '%2-3m%' AND UCASE(name) = '" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
    $count_2m_3m = $record->count_2m_3m;
    break;
  }
  $canopy_height_2m_3m = (float) ($count_2m_3m / $total_records_by_name) * 100;
  $object->canopy_height_2m_3m = (int) $canopy_height_2m_3m;
  
  
  $result = db_query("SELECT COUNT(ID) as count_greater_3m FROM rhm_input_data WHERE UCASE(canopy_height) like '%>3m%' AND UCASE(name) = '" . trim(strtoupper($name)) ."'");
  foreach ($result as $record){
    $count_greater_3m = $record->count_greater_3m;
    break;
  }
  $canopy_height_greater_3m = (float) ($count_greater_3m / $total_records_by_name) * 100;
  $object->canopy_height_greater_3m = (int) $canopy_height_greater_3m;
  
  
  return $object;
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $name
 */
function get_output_value_RHM_record($name) {
  $name = strtoupper($name);
  $total_records_by_name = get_number_of_record_follow_by_name($name);
  
  //$object_1 = get_group_1_for_output_data_RHM($name);
  $object_1 = get_group_1_for_output_data_RHM_2($name);
  $total_objects->bare_ground_1_percent = $object_1->bare_ground_1_percent;
  $total_objects->veg_cover_percent = $object_1->veg_cover_percent;
  
  $objects = get_group_2_for_output_data_RHM($name);
  
  if ($objects != 0) {
    $total_objects->bare_ground_2 = $objects->bare_ground_2;
    $total_objects->perennial_grasses = $objects->perennial_grasses;
    $total_objects->tree = $objects->tree;
    $total_objects->shrubs = $objects->shrubs;
    $total_objects->sub_shrubs = $objects->sub_shrubs;
    $total_objects->annual = $objects->annual;
    $total_objects->herb_litter = $objects->herb_litter;
    $total_objects->wood_litter = $objects->wood_litter;
    $total_objects->rock = $objects->rock;
  } else {
    $total_objects->bare_ground_2 = 0;
    $total_objects->perennial_grasses = 0;
    $total_objects->tree = 0;
    $total_objects->shrubs = 0;
    $total_objects->sub_shrubs = 0;
    $total_objects->annual = 0;
    $total_objects->herb_litter = 0;
    $total_objects->wood_litter = 0;
    $total_objects->rock = 0;
  }
  
  $object_3 = get_group_3_for_output_data_RHM($name,$total_records_by_name);
  $total_objects->canopy_gap_percent = $object_3->canopy_gap_percent;
  $total_objects->basal_gap_percent = $object_3->basal_gap_percent;
  
  
  $object_4 = get_group_4_for_output_data_RHM($name,$total_records_by_name);
  $total_objects->species_1_density_percent = $object_4->species_1_density_percent;
  $total_objects->species_2_density_percent = $object_4->species_2_density_percent;
  
  $object_5 = get_group_5_for_output_data_RHM($name, $total_records_by_name);
  $total_objects->canopy_height_smaller_10_cm = $object_5->canopy_height_smaller_10_cm;
  $total_objects->canopy_height_10_50_cm = $object_5->canopy_height_10_50_cm;
  $total_objects->canopy_height_50cm_1m = $object_5->canopy_height_50cm_1m;
  $total_objects->canopy_height_1m_2m = $object_5->canopy_height_1m_2m;
  $total_objects->canopy_height_2m_3m = $object_5->canopy_height_2m_3m;
  $total_objects->canopy_height_greater_3m = $object_5->canopy_height_greater_3m;
  $total_objects->total_record_consider = $total_records_by_name;
  
  return $total_objects;
}
/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $record_id
 * @param unknown_type $name
 * @param unknown_type $object
 */
function insert_rhm_output_data($record_id,$name, $object){
  $transaction = db_transaction();
  try {
    /* Write transaction */
    $nid = db_insert('rhm_ouput_summary_data')
    ->fields(array(
                    'record_id' =>  $record_id,
                    'name' => $name,
                    'total_record_consider' => $object->total_record_consider,
                    'bare_ground_1_percent' => $object->bare_ground_1_percent,
                    'veg_cover_percent' => $object->veg_cover_percent,
                    'bare_ground_2_percent' => $object->bare_ground_2,
                    'perennial_grass_percent' => $object->perennial_grasses,
                    'tree_percent' => $object->tree,
                    'shrub_percent' => $object->shrubs,
                    'sub_shrub_percent' => $object->sub_shrubs,
                    'annual_percent' => $object->annual,
                    'herb_litter_percent' => $object->herb_litter,
                    'wood_litter_percent' => $object->wood_litter,
                    'rock_percent' => $object->rock,
                    'canopy_gap_percent'=> $object->canopy_gap_percent,
                    'basal_gap_percent' => $object->basal_gap_percent,
                    'species_1_density' => $object->species_1_density_percent,
                    'species_2_density' => $object->species_2_density_percent,
                    'height_class_10cm' => $object->canopy_height_smaller_10_cm,
                    'height_class_10cm_50cm' =>  $object->canopy_height_10_50_cm,
                    'height_class_50cm_1m' => $object->canopy_height_50cm_1m,
                    'height_class_1m_2m' => $object->canopy_height_1m_2m,
                    'height_class_2m_3m' => $object->canopy_height_2m_3m,
                    'height_class_3m' => $object->canopy_height_greater_3m,
    ))
    ->execute();
    return $nid;
  } catch(Exception $ex){
    $transaction->rollback();
    echo $ex;
    return 0;
  }
}

/**
 * Nguyen Hai Thanh
 * Enter description here ...
 * @param unknown_type $name
 * @param unknown_type $recoder_name
 * @param unknown_type $transect
 * @param unknown_type $segment
 * @param unknown_type $date
 * @param unknown_type $canopy_height
 * @param unknown_type $canopy_gap
 * @param unknown_type $basal_gap
 * @param unknown_type $species_1_density
 * @param unknown_type $species_2_density
 * @param unknown_type $species_list
 * @param unknown_type $stick_segment_0
 * @param unknown_type $stick_segment_1
 * @param unknown_type $stick_segment_2
 * @param unknown_type $stick_segment_3
 * @param unknown_type $stick_segment_4
 * @param unknown_type $bare_total
 * @param unknown_type $trees_total
 * @param unknown_type $shrubs_total
 * @param unknown_type $sub_shrubs_total
 * @param unknown_type $perennial_grasses_total
 * @param unknown_type $annuals_total
 * @param unknown_type $herb_litter_total
 * @param unknown_type $wood_litter_total
 * @param unknown_type $rock_total
 * @param unknown_type $ip_address
 */
function insert_rhm_input_data_from_apps_to_server($name, $recorder_name, $transect, $segment, $date, $canopy_height, $canopy_gap, $basal_gap, $species_1_density, $species_2_density, $species_list, $stick_segment_0, $stick_segment_1, $stick_segment_2, $stick_segment_3, $stick_segment_4, $bare_total, $trees_total, $shrubs_total, $sub_shrubs_total, $perennial_grasses_total, $annuals_total, $herb_litter_total, $wood_litter_total, $rock_total, $ip_address) {
  $transaction = db_transaction();
  try {
    /* Write transaction */
    $date_thanhnh = date('Y-m-d h:i:s', time());
    $time = time();
    $nid = db_insert('rhm_input_data')
    ->fields(array(
                    'name' =>  $name,
                    'recorder_name' => $recorder_name,
                    'transect' => $transect,
                    'segment' => $segment,
                    'date' => $date,
                    'canopy_height' => $canopy_height,
                    'canopy_gap' => $canopy_gap,
                    'basal_gap' => $basal_gap,
                    'species_1_density' => $species_1_density,
                    'species_2_density' => $species_2_density,
                    'species_list' => $species_list,
                    'stick_segment_0' => $stick_segment_0,
                    'stick_segment_1' => $stick_segment_1,
                    'stick_segment_2' => $stick_segment_2,
                    'stick_segment_3' => $stick_segment_3,
                    'stick_segment_4' => $stick_segment_4,
                    'bare_total' => $bare_total,
                    'trees_total' => $trees_total,
                    'shrubs_total' => $shrubs_total,
                    'sub_shrubs_total' => $sub_shrubs_total,
                    'perennial_grasses_total' => $perennial_grasses_total,
                    'annuals_total' => $annuals_total,
                    'herb_litter_total' => $herb_litter_total,
                    'wood_litter_total' => $wood_litter_total,
                    'rock_total' => $rock_total,
                    'insert_unix_time' => $time,
                    'insert_normal_time' => $date_thanhnh,
                    'ip_address' => $ip_address,
    ))
    ->execute();
    return $nid;
  } catch(Exception $ex){
    $transaction->rollback();
    echo $ex;
    return 0;
  }
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $invitee_id
 * @param unknown_type $new_status
 */

function insert_landpks_input_data_from_apps_to_server($name, $recorder_name, $organization, $latitude, $longitude, $city, $modified_date, $land_cover, $grazed, $b_grazed, $flooding, $b_flooding, $slope, $slope_shape, $rock_fragment_for_soil_horizon_1, $rock_fragment_for_soil_horizon_2, $rock_fragment_for_soil_horizon_3, $rock_fragment_for_soil_horizon_4, $rock_fragment_for_soil_horizon_5, $rock_fragment_for_soil_horizon_6, $rock_fragment_for_soil_horizon_7 ,$color_for_soil_horizon_1, $color_for_soil_horizon_2 , $color_for_soil_horizon_3, $color_for_soil_horizon_4, $color_for_soil_horizon_5, $color_for_soil_horizon_6, $color_for_soil_horizon_7 ,$texture_for_soil_horizon_1, $texture_for_soil_horizon_2, $texture_for_soil_horizon_3, $texture_for_soil_horizon_4, $texture_for_soil_horizon_5, $texture_for_soil_horizon_6, $texture_for_soil_horizon_7 , $surface_cracking, $b_surface_cracking, $surface_salt, $b_surface_salt, $ip_address){
  $transaction = db_transaction();
  try {
    /* Write transaction */
    $date = date('Y-m-d h:i:s', time());
    $time = time();
    $nid = db_insert('landpks_input_data')
    ->fields(array(
                     'name' =>  $name,
                     'recorder_name' => $recorder_name,
                     'organization' => $organization,
                     'latitude' => $latitude,
                     'longitude' => $longitude,
                     'city' => $city,
                     'modified_date' => $modified_date,
                     'land_cover' => $land_cover,
                     'grazed' => $grazed,
                     'boolean_grazed' => $b_grazed,
                     'flooding' => $flooding,
                     'boolean_flooding' => $b_flooding,
                     'slope' => $slope,
                     'slope_shape' => $slope_shape,
                     'rock_fragment_for_soil_horizon_1' => $rock_fragment_for_soil_horizon_1,
                     'rock_fragment_for_soil_horizon_2' => $rock_fragment_for_soil_horizon_2,
                     'rock_fragment_for_soil_horizon_3' => $rock_fragment_for_soil_horizon_3,
                     'rock_fragment_for_soil_horizon_4' => $rock_fragment_for_soil_horizon_4,
                     'rock_fragment_for_soil_horizon_5' => $rock_fragment_for_soil_horizon_5,
                     'rock_fragment_for_soil_horizon_6' => $rock_fragment_for_soil_horizon_6,
                     'rock_fragment_for_soil_horizon_7' => $rock_fragment_for_soil_horizon_7,
                     'color_for_soil_horizon_1' => $color_for_soil_horizon_1,   
                     'color_for_soil_horizon_2' => $color_for_soil_horizon_2,
                     'color_for_soil_horizon_3' => $color_for_soil_horizon_3,
                     'color_for_soil_horizon_4' => $color_for_soil_horizon_4,   
                     'color_for_soil_horizon_5' => $color_for_soil_horizon_5,
                     'color_for_soil_horizon_6' => $color_for_soil_horizon_6,
                     'color_for_soil_horizon_7' => $color_for_soil_horizon_7,
                     'texture_for_soil_horizon_1' => $texture_for_soil_horizon_1,
                     'texture_for_soil_horizon_2' => $texture_for_soil_horizon_2,
                     'texture_for_soil_horizon_3' => $texture_for_soil_horizon_3,
                     'texture_for_soil_horizon_4' => $texture_for_soil_horizon_4,
                     'texture_for_soil_horizon_5' => $texture_for_soil_horizon_5,
                     'texture_for_soil_horizon_6' => $texture_for_soil_horizon_6,
                     'texture_for_soil_horizon_7' => $texture_for_soil_horizon_7,
                     'surface_cracking' => $surface_cracking,
                     'boolean_surface_cracking' => $b_surface_cracking,
                     'surface_salt' => $surface_salt,
                     'boolean_surface_salt' => $b_surface_salt,
                     'insert_unix_time' => $time,
                     'insert_normal_time' => $date,
                     'ip_address' => $ip_address,
    ))
    ->execute();
    return $nid;
  } catch(Exception $ex){
    $transaction->rollback();
    echo $ex;
    return 0;
  }
}


/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $video_version_id
 */
function check_exit_name($name){
  $result = db_query("SELECT 1 as rs FROM landpks_input_data WHERE name ='" . trim($name) ."'");
  foreach ($result as $record){
    if ($record->rs == 1){
      return true;
    }
  }
  return false;
}



/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $record_id
 */
function get_raw_output_data_NO_APEX_output($record_id){
  $sql = "SELECT gdal.record_id as record_id, gdal.record_name as record_name, gdal.topog_elevation as old_elevation, gdal.clim_gdd as gdd, gdal.clim_aridity_index as aridity, gdal.clim_fao_lgp as fao_lgp";
  $sql .= " FROM landpks_gdal_data_global_level gdal";
  $sql .= " WHERE gdal.record_id = $record_id";
  $results = db_query($sql);
  $gdal_data = null;
  foreach ($results as $record){
    $gdal_data = $record;
  }
  
  $sql = "SELECT awc.soil_profile_awc as soil_profile_awc";
  $sql .= " FROM  landpks_rosetta_awc_output_data awc";
  $sql .= " WHERE  awc.record_id = $record_id";
  $results = db_query($sql);
  
  $awc_data = null;
  foreach ($results as $record){
    $awc_data = $record;
  }
  
  
  $sql = "SELECT climate_precip_jan,climate_precip_feb,climate_precip_mar,climate_precip_apr,climate_precip_may,climate_precip_jun,climate_precip_jul,climate_precip_aug,climate_precip_sep,climate_precip_oct,climate_precip_dec,climate_precip_nov";
  $sql .= " FROM  landpks_climate_precip_summary";
  $sql .= " WHERE record_id = $record_id";
  $results = db_query($sql);
  
  $precip_data = null;
  foreach ($results as $record){
    $precip_data = $record;
  }
  
  
  $sql = "SELECT climate_avg_temp_jan,climate_avg_temp_feb,climate_avg_temp_mar,climate_avg_temp_apr,climate_avg_temp_may,climate_avg_temp_jun,climate_avg_temp_jul,climate_avg_temp_aug,climate_avg_temp_sep,climate_avg_temp_oct,climate_avg_temp_nov,climate_avg_temp_dec";
  $sql .= " FROM  landpks_climate_average_temp_summary";
  $sql .= " WHERE record_id = $record_id";
  $results = db_query($sql);
  
  $avg_temp_data = null;
  foreach ($results as $record){
    $avg_temp_data = $record;
  }
  
  
  
  $sql = "SELECT climate_max_temp_jan,climate_max_temp_feb,climate_max_temp_mar,climate_max_temp_apr,climate_max_temp_may,climate_max_temp_jun,climate_max_temp_jul,climate_max_temp_aug,climate_max_temp_sep,climate_max_temp_oct,climate_max_temp_nov,climate_max_temp_dec";
  $sql .= " FROM  landpks_climate_max_temp_summary";
  $sql .= " WHERE record_id = $record_id";
  $results = db_query($sql);
  
  $max_temp_data = null;
  foreach ($results as $record){
    $max_temp_data = $record;
  }
  
  
  $sql = "SELECT climate_min_temp_jan,climate_min_temp_feb,climate_min_temp_mar,climate_min_temp_apr,climate_min_temp_may,climate_min_temp_jun,climate_min_temp_jul,climate_min_temp_aug,climate_min_temp_sep,climate_min_temp_oct,climate_min_temp_nov,climate_min_temp_dec";
  $sql .= " FROM  landpks_climate_min_temp_summary";
  $sql .= " WHERE record_id = $record_id";
  $results = db_query($sql);
  $min_temp_data = null;
  foreach ($results as $record){
    $min_temp_data = $record;
  }
  
  if ($gdal_data != NULL && count($gdal_data) > 0){
     $final_record->record_id = $gdal_data->record_id;
     $final_record->record_name = $gdal_data->record_name;
     $final_record->old_elevation = $gdal_data->old_elevation;
     $final_record->gdd = $gdal_data->gdd;
     $final_record->aridity = $gdal_data->aridity;
     $final_record->fao_lgp = get_value_fao_lgp_from_gdal_value($gdal_data->fao_lgp, "ACCESS_DATABASE");
  } else {
     $final_record->record_id = -999;
     $final_record->record_name = -999;
     $final_record->old_elevation = -999;
     $final_record->gdd = -999;
     $final_record->aridity = -999; 
     $final_record->fao_lgp = -999;
  }
  
  if ($awc_data != NULL && count($awc_data) > 0){
     $final_record->soil_profile_awc = $awc_data->soil_profile_awc;
  } else {
     $final_record->soil_profile_awc = -999; 
  }
  
  if ($precip_data != NULL && count($precip_data) > 0){
    $final_record->climate_precip_jan = $precip_data->climate_precip_jan;
    $final_record->climate_precip_feb = $precip_data->climate_precip_feb;
    $final_record->climate_precip_mar = $precip_data->climate_precip_mar;
    $final_record->climate_precip_apr = $precip_data->climate_precip_apr;
    $final_record->climate_precip_may = $precip_data->climate_precip_may;
    $final_record->climate_precip_jun = $precip_data->climate_precip_jun;
    $final_record->climate_precip_jul = $precip_data->climate_precip_jul;
    $final_record->climate_precip_aug = $precip_data->climate_precip_aug;
    $final_record->climate_precip_sep = $precip_data->climate_precip_sep;
    $final_record->climate_precip_oct = $precip_data->climate_precip_oct;
    $final_record->climate_precip_nov = $precip_data->climate_precip_nov;
    $final_record->climate_precip_dec = $precip_data->climate_precip_dec;
    $final_record->climate_precip_annual = $final_record->climate_precip_jan + $final_record->climate_precip_feb + 
                                           $final_record->climate_precip_mar + $final_record->climate_precip_apr + 
                                           $final_record->climate_precip_may + $final_record->climate_precip_jun + 
                                           $final_record->climate_precip_jul + $final_record->climate_precip_aug +
                                           $final_record->climate_precip_sep + $final_record->climate_precip_oct + 
                                           $final_record->climate_precip_nov + $final_record->climate_precip_dec;
      
  } else {
    $final_record->climate_precip_jan = -999;
    $final_record->climate_precip_feb = -999;
    $final_record->climate_precip_mar = -999;
    $final_record->climate_precip_apr = -999;
    $final_record->climate_precip_may = -999;
    $final_record->climate_precip_jun = -999;
    $final_record->climate_precip_jul = -999;
    $final_record->climate_precip_aug = -999;
    $final_record->climate_precip_sep = -999;
    $final_record->climate_precip_oct = -999;
    $final_record->climate_precip_nov = -999;
    $final_record->climate_precip_dec = -999;
    $final_record->climate_precip_annual = -999;
  }
  
  
  if ($avg_temp_data != NULL && count($avg_temp_data) > 0){
    $final_record->climate_avg_temp_jan = $avg_temp_data->climate_avg_temp_jan;
    $final_record->climate_avg_temp_feb = $avg_temp_data->climate_avg_temp_feb;
    $final_record->climate_avg_temp_mar = $avg_temp_data->climate_avg_temp_mar;
    $final_record->climate_avg_temp_apr = $avg_temp_data->climate_avg_temp_apr;
    $final_record->climate_avg_temp_may = $avg_temp_data->climate_avg_temp_may;
    $final_record->climate_avg_temp_jun = $avg_temp_data->climate_avg_temp_jun;
    $final_record->climate_avg_temp_jul = $avg_temp_data->climate_avg_temp_jul;
    $final_record->climate_avg_temp_aug = $avg_temp_data->climate_avg_temp_aug;
    $final_record->climate_avg_temp_sep = $avg_temp_data->climate_avg_temp_sep;
    $final_record->climate_avg_temp_oct = $avg_temp_data->climate_avg_temp_oct;
    $final_record->climate_avg_temp_nov = $avg_temp_data->climate_avg_temp_nov;
    $final_record->climate_avg_temp_dec = $avg_temp_data->climate_avg_temp_dec;
  } else {
    $final_record->climate_avg_temp_jan = -999;
    $final_record->climate_avg_temp_feb = -999;
    $final_record->climate_avg_temp_mar = -999;
    $final_record->climate_avg_temp_apr = -999;
    $final_record->climate_avg_temp_may = -999;
    $final_record->climate_avg_temp_jun = -999;
    $final_record->climate_avg_temp_jul = -999;
    $final_record->climate_avg_temp_aug = -999;
    $final_record->climate_avg_temp_sep = -999;
    $final_record->climate_avg_temp_oct = -999;
    $final_record->climate_avg_temp_nov = -999;
    $final_record->climate_avg_temp_dec = -999;
  }
  
  
  if ($max_temp_data != NULL && count($max_temp_data) > 0){
    $final_record->climate_max_temp_jan = $max_temp_data->climate_max_temp_jan;
    $final_record->climate_max_temp_feb = $max_temp_data->climate_max_temp_feb;
    $final_record->climate_max_temp_mar = $max_temp_data->climate_max_temp_mar;
    $final_record->climate_max_temp_apr = $max_temp_data->climate_max_temp_apr;
    $final_record->climate_max_temp_may = $max_temp_data->climate_max_temp_may;
    $final_record->climate_max_temp_jun = $max_temp_data->climate_max_temp_jun;
    $final_record->climate_max_temp_jul = $max_temp_data->climate_max_temp_jul;
    $final_record->climate_max_temp_aug = $max_temp_data->climate_max_temp_aug;
    $final_record->climate_max_temp_sep = $max_temp_data->climate_max_temp_sep;
    $final_record->climate_max_temp_oct = $max_temp_data->climate_max_temp_oct;
    $final_record->climate_max_temp_nov = $max_temp_data->climate_max_temp_nov;
    $final_record->climate_max_temp_dec = $max_temp_data->climate_max_temp_dec;
  } else {
    $final_record->climate_max_temp_jan = -999;
    $final_record->climate_max_temp_feb = -999;
    $final_record->climate_max_temp_mar = -999;
    $final_record->climate_max_temp_apr = -999;
    $final_record->climate_max_temp_may = -999;
    $final_record->climate_max_temp_jun = -999;
    $final_record->climate_max_temp_jul = -999;
    $final_record->climate_max_temp_aug = -999;
    $final_record->climate_max_temp_sep = -999;
    $final_record->climate_max_temp_oct = -999;
    $final_record->climate_max_temp_nov = -999;
    $final_record->climate_max_temp_dec = -999;
  }

  if ($min_temp_data != NULL && count($min_temp_data) > 0){
    $final_record->climate_min_temp_jan = $min_temp_data->climate_min_temp_jan;
    $final_record->climate_min_temp_feb = $min_temp_data->climate_min_temp_feb;
    $final_record->climate_min_temp_mar = $min_temp_data->climate_min_temp_mar;
    $final_record->climate_min_temp_apr = $min_temp_data->climate_min_temp_apr;
    $final_record->climate_min_temp_may = $min_temp_data->climate_min_temp_may;
    $final_record->climate_min_temp_jun = $min_temp_data->climate_min_temp_jun;
    $final_record->climate_min_temp_jul = $min_temp_data->climate_min_temp_jul;
    $final_record->climate_min_temp_aug = $min_temp_data->climate_min_temp_aug;
    $final_record->climate_min_temp_sep = $min_temp_data->climate_min_temp_sep;
    $final_record->climate_min_temp_oct = $min_temp_data->climate_min_temp_oct;
    $final_record->climate_min_temp_nov = $min_temp_data->climate_min_temp_nov;
    $final_record->climate_min_temp_dec = $min_temp_data->climate_min_temp_dec;
  } else {
    $final_record->climate_min_temp_jan = -999;
    $final_record->climate_min_temp_feb = -999;
    $final_record->climate_min_temp_mar = -999;
    $final_record->climate_min_temp_apr = -999;
    $final_record->climate_min_temp_may = -999;
    $final_record->climate_min_temp_jun = -999;
    $final_record->climate_min_temp_jul = -999;
    $final_record->climate_min_temp_aug = -999;
    $final_record->climate_min_temp_sep = -999;
    $final_record->climate_min_temp_oct = -999;
    $final_record->climate_min_temp_nov = -999;
    $final_record->climate_min_temp_dec = -999;
  }
  
  
  return $final_record;
}


/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $record_id
 */
function get_raw_output_data_from_apex_output($record_id){
  //$record_name = standard_string_prevent_sql_injection($record_name);
  $sql = "SELECT ID, record_id, record_name, apex_output_y_maize, apex_output_yldg_maize, apex_output_y_glass, apex_output_yldg_glass";
  $sql .= " FROM lanpks_apex_output_data WHERE record_id = " . $record_id;
  $sql .= " ORDER BY ID DESC";

  $results = db_query($sql);
  $i = 0;
  foreach ($results as $record){
    return $record;
  }
}
/**
 * 
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $record_name
 * @param unknown_type $number_of_record
 */
function get_list_analytics_data_from_apex_output_and_relative_calculation_model($record_name,$number_of_record){
  $record_name = standard_string_prevent_sql_injection($record_name);
  $sql = "SELECT ID, record_id, maize_productivity, maize_erosion, glass_productivity, glass_erosion";
  $sql .= " FROM lanpks_apex_output_data WHERE UCASE(record_name) = '".strtoupper($record_name)."'";
  $sql .= " ORDER BY ID DESC LIMIT 0, " . $number_of_record;

  $results = db_query($sql);
  $i = 0;
  foreach ($results as $record){
    $options[$i] = array(
		    'ID' => $record->ID,
			'record_id'=> $record->record_id,
			'maize_productivity'=>$record->maize_productivity,
            'maize_erosion'=>$record->maize_erosion,
		    'glass_productivity'=> $record->glass_productivity,
		    'glass_erosion'=>$record->glass_erosion,
    );
    $i++;
  }
  return $options;
}
/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param $price_set_id
 */
function get_all_landpks_input_data_from_mobile_order_by($type){
  if ($type == 1){
    $sql = "SELECT ID, name, latitude, longitude, insert_normal_time, ip_address ";
    $sql .= "FROM landpks_input_data ";
    $sql .= "ORDER BY insert_unix_time DESC LIMIT 0,100";
  }

  //$results = db_query($sql,array(':gu'=>$price_set_id));
  $results = db_query($sql);
  $i = 0;
  foreach ($results as $record){
    //$price_plan = node_load($record->price_plan_id);
    $options[$i] = array(
		    'name' => $record->name,
			'latitude'=> $record->latitude,
			'longitude'=>$record->longitude,
			'insert_normal_time'=>$record->insert_normal_time,
            'ip_address'=>$record->ip_address,
		    'view'=> l('View',''),
		    'edit'=> l('Edit',''),
            'run'=> l('Run',''),
    );
    $i++;
  }
  return $options;
}
function call_python_script($ID, $x, $y, $record_name){
  /*
   $cmd = 'cd Python_APEX && cd 3_WISE_SOL_PROJECT && python C:\xampp\htdocs\APEX\Python_APEX\3_WISE_SOL_PROJECT\Run_All_HWSD.py -x ' . $x . ' -y ' . $y . ' -ID ' . $ID;
   $output = exec($cmd);
   $cmd = 'cd Python_APEX && cd 8_SITE_PROJECT && python C:\xampp\htdocs\APEX\Python_APEX\8_SITE_PROJECT\Run_All_SITE.py -x ' . $x . ' -y ' . $y . ' -ID ' . $ID;
   $output = exec($cmd);
   $cmd = 'cd Python_APEX && cd 2_WEATHER_PROJECT_REAL_TIME && python C:\xampp\htdocs\APEX\Python_APEX\2_WEATHER_PROJECT_REAL_TIME\Run_All_WEATHER.py -x ' . $x . ' -y ' . $y . ' -ID ' . $ID;
   $output = exec($cmd);
   $cmd = 'cd Python_APEX && cd 7_SUBAREA_PROJECT_REAL_TIME && python C:\xampp\htdocs\APEX\Python_APEX\7_SUBAREA_PROJECT_REAL_TIME\Run_All_SUBAREA.py -x ' . $x . ' -y ' . $y . ' -ID ' . $ID;
   $output = exec($cmd);
   $cmd = 'cd Python_APEX && cd 9_APEX_RUN && python C:\xampp\htdocs\APEX\Python_APEX\9_APEX_RUN\Run_All_APEX_RUN.py -x ' . $x . ' -y ' . $y . ' -ID ' . $ID;
   $output = exec($cmd);
   */
  $cmd = 'cd Python_APEX && cd 1_CONTROLLER_PROJECT && python C:\xampp\htdocs\APEX\Python_APEX\1_CONTROLLER_PROJECT\Run_main_CONTROLLER.py -x ' . $x . ' -y ' . $y . ' -ID ' . $ID . ' -name ' . $record_name;
  $output = exec($cmd);
  
  if ($output == "ERROR[100]:LOCATION_IS_NOT_SUPPORTED"){
    return -1;
  }
  return 1;
}



/***************************************************************************************/
/********************PHUC VU CHO THANG NGU SI*******************************************/
/***************************************************************************************/
/**
 * NGUYEN HAI THANH - Insert kieu moi cho thang ngu si
 * Enter description here ...
 * @param unknown_type $name
 * @param unknown_type $recorder_name
 * @param unknown_type $organization
 * @param unknown_type $latitude
 * @param unknown_type $longitude
 * @param unknown_type $city
 * @param unknown_type $modified_date
 * @param unknown_type $land_cover
 * @param unknown_type $grazed
 * @param unknown_type $b_grazed
 * @param unknown_type $flooding
 * @param unknown_type $b_flooding
 * @param unknown_type $slope
 * @param unknown_type $slope_shape
 * @param unknown_type $rock_fragment_for_soil_horizon_1
 * @param unknown_type $rock_fragment_for_soil_horizon_2
 * @param unknown_type $rock_fragment_for_soil_horizon_3
 * @param unknown_type $rock_fragment_for_soil_horizon_4
 * @param unknown_type $rock_fragment_for_soil_horizon_5
 * @param unknown_type $rock_fragment_for_soil_horizon_6
 * @param unknown_type $rock_fragment_for_soil_horizon_7
 * @param unknown_type $color_for_soil_horizon_1
 * @param unknown_type $color_for_soil_horizon_2
 * @param unknown_type $color_for_soil_horizon_3
 * @param unknown_type $color_for_soil_horizon_4
 * @param unknown_type $color_for_soil_horizon_5
 * @param unknown_type $color_for_soil_horizon_6
 * @param unknown_type $color_for_soil_horizon_7
 * @param unknown_type $texture_for_soil_horizon_1
 * @param unknown_type $texture_for_soil_horizon_2
 * @param unknown_type $texture_for_soil_horizon_3
 * @param unknown_type $texture_for_soil_horizon_4
 * @param unknown_type $texture_for_soil_horizon_5
 * @param unknown_type $texture_for_soil_horizon_6
 * @param unknown_type $texture_for_soil_horizon_7
 * @param unknown_type $surface_cracking
 * @param unknown_type $b_surface_cracking
 * @param unknown_type $surface_salt
 * @param unknown_type $b_surface_salt
 * @param unknown_type $ip_address
 */
function insert_landpks_input_plot_new($name, $recorder_name, $organization, $latitude, $longitude, $city, $modified_date, $land_cover, $grazed, $b_grazed, $flooding, $b_flooding, $slope, $slope_shape, $rock_fragment_for_soil_horizon_1, $rock_fragment_for_soil_horizon_2, $rock_fragment_for_soil_horizon_3, $rock_fragment_for_soil_horizon_4, $rock_fragment_for_soil_horizon_5, $rock_fragment_for_soil_horizon_6, $rock_fragment_for_soil_horizon_7 ,$color_for_soil_horizon_1, $color_for_soil_horizon_2 , $color_for_soil_horizon_3, $color_for_soil_horizon_4, $color_for_soil_horizon_5, $color_for_soil_horizon_6, $color_for_soil_horizon_7 ,$texture_for_soil_horizon_1, $texture_for_soil_horizon_2, $texture_for_soil_horizon_3, $texture_for_soil_horizon_4, $texture_for_soil_horizon_5, $texture_for_soil_horizon_6, $texture_for_soil_horizon_7 , $surface_cracking, $b_surface_cracking, $surface_salt, $b_surface_salt, $ip_address){
   
   try {
      /***Step 1 : Get Reference Data ***/ 
      $land_cover_category_id = get_landcover_category_id_from_landcover_data_plot_new($land_cover,"FREE_STYLE");
      $slope_category_id = get_slope_category_id_from_slope_value_plot_new($slope,"FREE_STYLE");
      $slope_shape_category_id = get_slope_shape_category_id_from_slope_shape_value_plot_new($slope_shape,"FREE_STYLE");
      
      /***Step 2 : Insert data plot to Input_Table ***/
      $transaction = db_transaction();
      $plot_id = 0;
      try {
        /* Write transaction */
        $date = date('Y-m-d h:i:s', time());
        $time = time();
        $plot_id = db_insert('new_landpks_input_plots')
        ->fields(array(
                         'name' =>  $name,
                         'recorder_name' => $recorder_name,
                         'organization' => $organization,
                         'latitude' => $latitude,
                         'longitude' => $longitude,
                         'city' => $city,
                         'modified_date' => $modified_date,
                         'landpks_landcover_category_id' => $land_cover_category_id,
                         'grazed' => $grazed,
                         'boolean_grazed' => $b_grazed,
                         'flooding' => $flooding,
                         'boolean_flooding' => $b_flooding,
                         'landpks_slope_category_id' => $slope_category_id,
                         'landpks_slope_shape_category_id' => $slope_shape_category_id,
                         'surface_cracking' => $surface_cracking,
                         'boolean_surface_cracking' => $b_surface_cracking,
                         'surface_salt' => $surface_salt,
                         'boolean_surface_salt' => $b_surface_salt,
                         'insert_unix_time' => $time,
                         'insert_normal_time' => $date,
                         'ip_address' => $ip_address,
        ))
        ->execute();
      } catch(Exception $ex){
        $transaction->rollback();
        //echo $ex;
        return 0;
      }
     /***Step 3 : Get data per each layer (7 layers) - Insert data to soil horizon ***/
     
     if ($plot_id != 0) {
       // Layer 1 
       $soil_horizon_depth_id_1 = 1;  //FIX : 0-1cm
       $soil_texture_category_id_1 = get_soil_texture_category_id_from_soil_texture_value_plot_new($texture_for_soil_horizon_1, "FREE_STYLE");
       $soil_rock_category_id_1 = get_soil_rock_category_id_from_soil_rock_value_plot_new($rock_fragment_for_soil_horizon_1,"FREE_STYLE");
       $insert_soil_horizon_1 = insert_landpks_input_soil_horizon_new($plot_id, "", $soil_horizon_depth_id_1, $soil_texture_category_id_1, $soil_rock_category_id_1, 0);
       
       // Layer 2 
       $soil_horizon_depth_id_2 = 2;  //FIX : 1-10cm
       $soil_texture_category_id_2 = get_soil_texture_category_id_from_soil_texture_value_plot_new($texture_for_soil_horizon_2, "FREE_STYLE");
       $soil_rock_category_id_2 = get_soil_rock_category_id_from_soil_rock_value_plot_new($rock_fragment_for_soil_horizon_2,"FREE_STYLE");
       $insert_soil_horizon_2 = insert_landpks_input_soil_horizon_new($plot_id, "", $soil_horizon_depth_id_2, $soil_texture_category_id_2, $soil_rock_category_id_2, 0);
       
       // Layer 3 
       $soil_horizon_depth_id_3 = 3;  //FIX : 10-20cm
       $soil_texture_category_id_3 = get_soil_texture_category_id_from_soil_texture_value_plot_new($texture_for_soil_horizon_3, "FREE_STYLE");
       $soil_rock_category_id_3 = get_soil_rock_category_id_from_soil_rock_value_plot_new($rock_fragment_for_soil_horizon_3,"FREE_STYLE");
       $insert_soil_horizon_3 = insert_landpks_input_soil_horizon_new($plot_id, "", $soil_horizon_depth_id_3, $soil_texture_category_id_3, $soil_rock_category_id_3, 0);
       
       // Layer 4 
       $soil_horizon_depth_id_4 = 4;  //FIX : 20-50cm
       $soil_texture_category_id_4 = get_soil_texture_category_id_from_soil_texture_value_plot_new($texture_for_soil_horizon_4, "FREE_STYLE");
       $soil_rock_category_id_4 = get_soil_rock_category_id_from_soil_rock_value_plot_new($rock_fragment_for_soil_horizon_4,"FREE_STYLE");
       $insert_soil_horizon_4 = insert_landpks_input_soil_horizon_new($plot_id, "", $soil_horizon_depth_id_4, $soil_texture_category_id_4, $soil_rock_category_id_4, 0);
       
       // Layer 5 
       $soil_horizon_depth_id_5 = 5;  //FIX : 50-70cm
       $soil_texture_category_id_5 = get_soil_texture_category_id_from_soil_texture_value_plot_new($texture_for_soil_horizon_5, "FREE_STYLE");
       $soil_rock_category_id_5 = get_soil_rock_category_id_from_soil_rock_value_plot_new($rock_fragment_for_soil_horizon_5,"FREE_STYLE");
       $insert_soil_horizon_5 = insert_landpks_input_soil_horizon_new($plot_id, "", $soil_horizon_depth_id_5, $soil_texture_category_id_5, $soil_rock_category_id_5, 0);
       
       // Layer 6 
       $soil_horizon_depth_id_6 = 6;  //FIX : 70-100cm
       $soil_texture_category_id_6 = get_soil_texture_category_id_from_soil_texture_value_plot_new($texture_for_soil_horizon_6, "FREE_STYLE");
       $soil_rock_category_id_6 = get_soil_rock_category_id_from_soil_rock_value_plot_new($rock_fragment_for_soil_horizon_6,"FREE_STYLE");
       $insert_soil_horizon_6 = insert_landpks_input_soil_horizon_new($plot_id, "", $soil_horizon_depth_id_6, $soil_texture_category_id_6, $soil_rock_category_id_6, 0);
       
       // Layer 7 
       $soil_horizon_depth_id_7 = 7;  //FIX : 100-120cm
       $soil_texture_category_id_7 = get_soil_texture_category_id_from_soil_texture_value_plot_new($texture_for_soil_horizon_7, "FREE_STYLE");
       $soil_rock_category_id_7 = get_soil_rock_category_id_from_soil_rock_value_plot_new($rock_fragment_for_soil_horizon_7,"FREE_STYLE");
       $insert_soil_horizon_7 = insert_landpks_input_soil_horizon_new($plot_id, "", $soil_horizon_depth_id_7, $soil_texture_category_id_7, $soil_rock_category_id_7, 0);
     } else {
       return 0;
     }
     
     
     return $plot_id;
   } catch(Exception $ex){
      //echo $ex;
      return 0;
   }
}
/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $int_plot_id
 * @param unknown_type $plot_id
 * @param unknown_type $landpks_soil_horizon_depth_id
 * @param unknown_type $landpks_soil_texture_category_id
 * @param unknown_type $landpks_soil_rock_fragment_category_id
 * @param unknown_type $color
 */
function insert_landpks_input_soil_horizon_new($int_plot_id, $plot_id, $landpks_soil_horizon_depth_id, $landpks_soil_texture_category_id, $landpks_soil_rock_fragment_category_id, $color) {
      $transaction = db_transaction();
      try {
        /* Write transaction */
        $soil_horizon_id = db_insert('new_landpks_soil_horizons')
        ->fields(array(
                         'int_plot_id' =>  $int_plot_id,
                         'plot_id' => $plot_id,
                         'landpks_soil_horizon_depth_id' => $landpks_soil_horizon_depth_id,
                         'landpks_soil_texture_category_id' => $landpks_soil_texture_category_id,
                         'landpks_soil_rock_fragment_category_id' => $landpks_soil_rock_fragment_category_id,
                         'color'=> $color,
        ))
        ->execute();
        return $soil_horizon_id;
      } catch(Exception $ex){
        $transaction->rollback();
        //echo $ex;
        return 0;
      }
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $name
 */
function get_landcover_category_id_from_landcover_data_plot_new($landcover_data,$way) {
  if (strtoupper($way) == "ACCESS_DATABASE"){
    $result = db_query("SELECT ID as rs FROM new_landpks_landcover_categories WHERE UCASE(landcover_value) = '" . trim(strtoupper($landcover_data)) ."'");
    foreach ($result as $record){
       return $record->rs;
    }
    return 0;
  } else {
    //if then else return
    return 1;
  }
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $name
 */
function get_slope_category_id_from_slope_value_plot_new($slope_value_data,$way) {
  if (strtoupper(trim($way)) == "ACCESS_DATABASE"){
    $result = db_query("SELECT ID as rs FROM new_landpks_slope_categories WHERE UCASE(slope_value) = '" . trim(strtoupper($slope_value_data)) ."'");
    foreach ($result as $record){
       return $record->rs;
    }
    return 0;
  } else {
    //if then else return
    return 2;
  }
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $name
 */
function get_slope_shape_category_id_from_slope_shape_value_plot_new($slope_shape_value_data,$way) {
  if (strtoupper(trim($way)) == "ACCESS_DATABASE"){
    $result = db_query("SELECT ID as rs FROM new_landpks_slope_shape_categories WHERE UCASE(slope_shape_value) = '" . trim(strtoupper($slope_shape_value_data)) ."'");
    foreach ($result as $record){
       return $record->rs;
    }
    return 0;
  } else {
     //if then else return
    return 3;
  }
}


/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $name
 */
function get_soil_horizon_depth_id_from_soil_horizon_depth_value_plot_new($soil_horizon_depth_value_data) {
  $result = db_query("SELECT ID as rs FROM new_landpks_soil_horizon_depths WHERE UCASE(soil_horizon_depth_value) = '" . trim(strtoupper($soil_horizon_depth_value_data)) ."'");
  foreach ($result as $record){
     return $record->rs;
  }
  return 0;
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $name
 */
function get_soil_texture_category_id_from_soil_texture_value_plot_new($soil_texture_value_data,$way) {
  if (strtoupper(trim($way)) == "ACCESS_DATABASE"){
    $result = db_query("SELECT ID as rs FROM new_landpks_soil_texture_categories WHERE UCASE(soil_texture_value) = '" . trim(strtoupper($soil_texture_value_data)) ."'");
    foreach ($result as $record){
       return $record->rs;
    }
    return 0;
  } else {
    //if then else return
    return 4;
  }
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $name
 */
function get_soil_rock_category_id_from_soil_rock_value_plot_new($soil_rock_value_data,$way) {
  if (strtoupper(trim($way)) == "ACCESS_DATABASE"){
     $result = db_query("SELECT ID as rs FROM new_landpks_soil_rock_fragment_categories WHERE UCASE(soil_rock_fragment_value) = '" . trim(strtoupper($soil_rock_value_data)) ."'");
     foreach ($result as $record){
       return $record->rs;
     }
     return 0;
  } else {
    //if then else return
    return 5;
  }
}


function update_plot_id_to_result_apex_table($result_good, $result_bad){
  $result = db_query("UPDATE lanpks_apex_output_data SET plot_id = $result_bad WHERE record_id = $result_good");
}

/**********************************************************************************************************************************/
/**********************************************************************************************************************************/
/*************************************************GDAL PROJECT**************************************************/
/**********************************************************************************************************************************/
/**********************************************************************************************************************************/
function get_list_gdal_record_country_level($record_id){
  $sql = "SELECT country_name, slope_percentage, slope_reclassified, plane_curvature, profile_curvature, curvature, dem, aspect";
  $sql .= " FROM landpks_gdal_data_country_level WHERE record_id = $record_id";
  $results = db_query($sql);
  foreach ($results as $record){
    return $record;
  }
  return NULL;
}

/*
 * GET List GDAL information
 */
function get_list_gdal_record_information($from_record_id,$to_record_id,$record_name,$country_code){
  $sql = "SELECT ID, record_id, plot_id, record_name, latitude, longitude, country_code_data, clim_slate_weather_data, clim_precipitation_data,";
  $sql .= " clim_gdd, clim_aridity_index, clim_kopgeiger, clim_fao_lgp, clim_modis_evapotrans, clim_precip_novdecjan, clim_precip_febmarapr, clim_precip_mayjunjul,";
  $sql .= " clim_precip_augsepoct, clim_wind_data_1, clim_wind_data_2, clim_wind_data_3, clim_wind_data_4, clim_wind_data_5, clim_wind_data_6, clim_wind_data_7,";
  $sql .= " clim_wind_data_8, clim_wind_data_9, clim_wind_data_10, clim_wind_data_11, clim_wind_data_12, soil_hwsd_data, soil_depth_gaez, soil_textclass_gaez, soil_fert_gaez as fert,";
  $sql .= " soil_workab_gaez, soil_toxic_gaez, topog_elevation, topog_aspect, topog_geolage, topog_dem_global, topog_dem_old, topog_slope_global, topog_landform_global,";
  $sql .= " topog_twi_global, topog_topi_global, topog_israd_global, landcover_modis_2001, landcover_modis_2002, landcover_modis_2004, landcover_modis_2010, landcover_modis_2011,";
  $sql .= " landcover_modis_2012, landcover_cult_gaez, landcover_irrcult_gaez, landcover_grass_gaez, landcover_protect_gaez, landcover_agnprotect_gaez, vegind_modis_evi_m,";
  $sql .= " vegind_modis_evi_sd, vegind_modis_lai_m, vegind_modis_lai_sd, manage_cerealsuit_low_gaez, manage_cerealsuit_hight_gaez, pop_density, afsis_topog_dem, afsis_topog_twi, afsis_topog_sca";
  $sql .= " FROM landpks_gdal_data_global_level";
  $sql .= " WHERE 1=1";
  $array_gdal = array();
  
  
  if (!isEmpty($record_name)){
    $sql .= " AND record_name='". $record_name ."'";
  }
  if (!isEmpty($from_record_id)) {
    $sql .= " AND record_id >= " . $from_record_id;
  }
  if (!isEmpty($to_record_id)) {
    $sql .= " AND record_id <= " . $to_record_id;
  }
  if (!isEmpty($country_code)){
     $sql .= " AND country_code_data = '". $country_code ."'";
  }
  $sql .= " ORDER BY ID DESC";
  
  $results = db_query($sql);
  
  $i = 0 ;
  foreach ($results as $record){
    $array_gdal[$i]->ID = $record->ID;
    $array_gdal[$i]->record_id = $record->record_id;
    $array_gdal[$i]->plot_id = $record->plot_id;
    $array_gdal[$i]->record_name = $record->record_name;
    $array_gdal[$i]->latitude = $record->latitude;
    $array_gdal[$i]->longitude = $record->longitude;
    $array_gdal[$i]->country_code_data = $record->country_code_data; 
    $array_gdal[$i]->country_name = get_country_name_from_country_code_lookup($record->country_code_data);
    $array_gdal[$i]->clim_slate_weather_data = $record->clim_slate_weather_data; 
    $array_gdal[$i]->clim_precipitation_data = $record->clim_precipitation_data; 
    $array_gdal[$i]->clim_gdd = $record->clim_gdd; 
    $array_gdal[$i]->clim_aridity_index = $record->clim_aridity_index; 
    $array_gdal[$i]->clim_kopgeiger = $record->clim_kopgeiger; 
    $array_gdal[$i]->clim_kopgeiger_detail = get_value_worldkgeiger_from_gdal_value($record->clim_kopgeiger, "ACCESS_DATABASE");
    $array_gdal[$i]->clim_fao_lgp = $record->clim_fao_lgp; 
    $array_gdal[$i]->clim_fao_lgp_detail = get_value_fao_lgp_from_gdal_value($record->clim_fao_lgp,"ACCESS_DATABASE"); 
    $array_gdal[$i]->clim_modis_evapotrans = $record->clim_modis_evapotrans; 
    $array_gdal[$i]->clim_precip_novdecjan = $record->clim_precip_novdecjan; 
    $array_gdal[$i]->clim_precip_febmarapr = $record->clim_precip_febmarapr; 
    $array_gdal[$i]->clim_precip_mayjunjul = $record->clim_precip_mayjunjul; 
    $array_gdal[$i]->clim_precip_augsepoct = $record->clim_precip_augsepoct; 
    $array_gdal[$i]->clim_wind_data_1 = $record->clim_wind_data_1; 
    $array_gdal[$i]->clim_wind_data_2 = $record->clim_wind_data_2; 
    $array_gdal[$i]->clim_wind_data_3 = $record->clim_wind_data_3; 
    $array_gdal[$i]->clim_wind_data_4 = $record->clim_wind_data_4; 
    $array_gdal[$i]->clim_wind_data_5 = $record->clim_wind_data_5; 
    $array_gdal[$i]->clim_wind_data_6 = $record->clim_wind_data_6; 
    $array_gdal[$i]->clim_wind_data_7 = $record->clim_wind_data_7; 
    $array_gdal[$i]->clim_wind_data_8 = $record->clim_wind_data_8; 
    $array_gdal[$i]->clim_wind_data_9 = $record->clim_wind_data_9; 
    $array_gdal[$i]->clim_wind_data_10 = $record->clim_wind_data_10; 
    $array_gdal[$i]->clim_wind_data_11 = $record->clim_wind_data_11; 
    $array_gdal[$i]->clim_wind_data_12 = $record->clim_wind_data_12; 
    $array_gdal[$i]->soil_hwsd_data = $record->soil_hwsd_data; 
    $array_gdal[$i]->soil_depth_gaez = $record->soil_depth_gaez;
    $array_gdal[$i]->soil_depth_gaez_detail = get_value_soil_depth_gaez_from_gdal_value($record->soil_depth_gaez, "ACCESS_DATABASE");
    $array_gdal[$i]->soil_textclass_gaez = $record->soil_textclass_gaez;
    $array_gdal[$i]->soil_textclass_gaez_detail = get_value_soil_textureclass_from_gdal_value($record->soil_textclass_gaez,"ACCESS_DATABASE");
    $array_gdal[$i]->soil_fert_gaez = $record->fert;
    $array_gdal[$i]->soil_fert_gaez_detail = get_value_soil_fert_gaez_from_gdal_value($record->fert,"ACCESS_DATABASE");
    $array_gdal[$i]->soil_workab_gaez = $record->soil_workab_gaez;
    $array_gdal[$i]->soil_workab_gaez_detail = get_value_soil_workab_gaez_from_gdal_value($record->soil_workab_gaez,"ACCESS_DATABASE");
    $array_gdal[$i]->soil_toxic_gaez = $record->soil_toxic_gaez;
    $array_gdal[$i]->soil_toxic_gaez_detail = get_value_soil_toxic_gaez_from_gdal_value($record->soil_toxic_gaez,"ACCESS_DATABASE");
    $array_gdal[$i]->topog_elevation = $record->topog_elevation;
    $array_gdal[$i]->topog_aspect = $record->topog_aspect;
    $array_gdal[$i]->topog_geolage = $record->topog_geolage;
    $array_gdal[$i]->topog_dem_global = $record->topog_dem_global;
    $array_gdal[$i]->topog_dem_old = $record->topog_dem_old;
    $array_gdal[$i]->topog_slope_global = $record->topog_slope_global;
    $array_gdal[$i]->topog_landform_global = $record->topog_landform_global;
    $array_gdal[$i]->topog_twi_global = $record->topog_twi_global;
    $array_gdal[$i]->topog_topi_global = $record->topog_topi_global;

    $array_gdal[$i]->topog_israd_global = $record->topog_israd_global;
    $array_gdal[$i]->landcover_modis_2001 = $record->landcover_modis_2001;
    $array_gdal[$i]->landcover_modis_2001_detail = get_value_landcover_modis_from_gdal_value($record->landcover_modis_2001,"ACCESS_DATABASE");
    $array_gdal[$i]->landcover_modis_2002 = $record->landcover_modis_2002;
    $array_gdal[$i]->landcover_modis_2002_detail = get_value_landcover_modis_from_gdal_value($record->landcover_modis_2002,"ACCESS_DATABASE");
    $array_gdal[$i]->landcover_modis_2004 = $record->landcover_modis_2004;
    $array_gdal[$i]->landcover_modis_2004_detail = get_value_landcover_modis_from_gdal_value($record->landcover_modis_2004,"ACCESS_DATABASE");
    $array_gdal[$i]->landcover_modis_2010 = $record->landcover_modis_2010;
    $array_gdal[$i]->landcover_modis_2010_detail = get_value_landcover_modis_from_gdal_value($record->landcover_modis_2010,"ACCESS_DATABASE");
    $array_gdal[$i]->landcover_modis_2011 = $record->landcover_modis_2011;
    $array_gdal[$i]->landcover_modis_2011_detail = get_value_landcover_modis_from_gdal_value($record->landcover_modis_2011,"ACCESS_DATABASE");
    $array_gdal[$i]->landcover_modis_2012 = $record->landcover_modis_2012;
    $array_gdal[$i]->landcover_modis_2012_detail = get_value_landcover_modis_from_gdal_value($record->landcover_modis_2012,"ACCESS_DATABASE");
    $array_gdal[$i]->landcover_cult_gaez = $record->landcover_cult_gaez;
    $array_gdal[$i]->landcover_irrcult_gaez = $record->landcover_irrcult_gaez;
    $array_gdal[$i]->landcover_grass_gaez = $record->landcover_grass_gaez;
    
    $array_gdal[$i]->landcover_protect_gaez = $record->landcover_protect_gaez;
    $array_gdal[$i]->landcover_protect_gaez_detail = get_value_protected_area_from_gdal_value($record->landcover_protect_gaez,"ACCESS_DATABASE");
    $array_gdal[$i]->landcover_agnprotect_gaez = $record->landcover_agnprotect_gaez;
    $array_gdal[$i]->landcover_agnprotect_gaez_detail = get_value_protected_agr_area_from_gdal_value($record->landcover_agnprotect_gaez,"ACCESS_DATABASE");
    $array_gdal[$i]->vegind_modis_evi_m = $record->vegind_modis_evi_m;
    $array_gdal[$i]->vegind_modis_evi_sd = $record->vegind_modis_evi_sd;
    $array_gdal[$i]->vegind_modis_lai_m = $record->vegind_modis_lai_m;
    $array_gdal[$i]->vegind_modis_lai_sd = $record->vegind_modis_lai_sd;
    $array_gdal[$i]->manage_cerealsuit_low_gaez = $record->manage_cerealsuit_low_gaez;
    $array_gdal[$i]->manage_cerealsuit_low_gaez_detail = get_value_cereal_from_gdal_value($record->manage_cerealsuit_low_gaez,"ACCESS_DATABASE");
    $array_gdal[$i]->manage_cerealsuit_hight_gaez = $record->manage_cerealsuit_hight_gaez;
    $array_gdal[$i]->manage_cerealsuit_hight_gaez_detail = get_value_cereal_from_gdal_value($record->manage_cerealsuit_hight_gaez,"ACCESS_DATABASE");
    $array_gdal[$i]->pop_density = $record->pop_density;
    $array_gdal[$i]->afsis_topog_dem = $record->afsis_topog_dem;
    $array_gdal[$i]->afsis_topog_twi = $record->afsis_topog_twi;
    $array_gdal[$i]->afsis_topog_sca = $record->afsis_topog_sca;
    
    
    $country_data = get_list_gdal_record_country_level($record->record_id);
    $array_gdal[$i]->country_name_2 = $country_data->country_name;
    $array_gdal[$i]->slope_percentage = $country_data->slope_percentage;
    $array_gdal[$i]->slope_reclassified = $country_data->slope_reclassified;
    $array_gdal[$i]->plane_curvature = $country_data->plane_curvature;
    $array_gdal[$i]->profile_curvature = $country_data->profile_curvature;
    $array_gdal[$i]->curvature = $country_data->curvature;
    $array_gdal[$i]->dem = $country_data->dem;
    $array_gdal[$i]->aspect = $country_data->aspect;
    
    $i++;
  }
  if ($i <> 0){
    return $array_gdal;
  } else {
    return false;
  }
}
/*
 * Get Lookup table Country Name
 */
function get_country_name_from_country_code_lookup($country_code){
  if ($country_code == '209' || $country_code == 209){
    return "KENYA"; 
  } else if ($country_code == '228' || $country_code == 228){
    return "NAMIBIA";
  } else {
    return "UN-KNOWN";
  }
}
/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $worldkgeiger_gdal
 */
function get_value_worldkgeiger_from_gdal_value($worldkgeiger_gdal,$way){
  if (strtoupper($way) == "ACCESS_DATABASE"){
     $result = db_query("SELECT landpks_gdal_worldkgeiger_lookup.count, landpks_gdal_worldkgeiger_lookup.desc, landpks_gdal_worldkgeiger_lookup.label FROM landpks_gdal_worldkgeiger_lookup WHERE gdal_value = " . $worldkgeiger_gdal);
     foreach ($result as $record){
       return $record->count. "-" .$record->desc . "-" . $record->label;
     }
     return "NONE";
  } else {
    return "NONE";
  }
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $worldkgeiger_gdal
 */
function get_value_fao_lgp_from_gdal_value($fao_lgp_gdal,$way){
  if (strtoupper($way) == "ACCESS_DATABASE"){
     $result = db_query("SELECT lgp_value as label FROM landpks_gdal_fao_lgp_lookup WHERE gdal_value = " . $fao_lgp_gdal);
     foreach ($result as $record){
       return $record->label;
     }
     return "NONE";
  } else {
    return "NONE";
  }
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $worldkgeiger_gdal
 */
function get_value_soil_textureclass_from_gdal_value($soil_textureclass_gdal,$way){
  if (strtoupper($way) == "ACCESS_DATABASE"){
     $result = db_query("SELECT texture_class_value as rs FROM landpks_gdal_soil_textclass_gaez_lookup WHERE gdal_value = " . $soil_textureclass_gdal);
     foreach ($result as $record){
       return $record->rs;
     }
     return "NONE";
  } else {
    return "NONE";
  }
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $worldkgeiger_gdal
 */
function get_value_soil_fert_gaez_from_gdal_value($soil_fert_gaez_gdal,$way){
  if (strtoupper($way) == "ACCESS_DATABASE"){
     $result = db_query("SELECT fertility_value as rs FROM landpks_gdal_soil_fert_gaez_lookup WHERE gdal_value = " . $soil_fert_gaez_gdal);
     foreach ($result as $record){
       return $record->rs;
     }
     return "NONE";
  } else {
    return "NONE";
  }
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $worldkgeiger_gdal
 */
function get_value_soil_workab_gaez_from_gdal_value($soil_workab_gaez_gdal,$way){
  if (strtoupper($way) == "ACCESS_DATABASE"){
     $result = db_query("SELECT workability_value as rs FROM landpks_gdal_soil_workab_gaez_lookup WHERE gdal_value = " . $soil_workab_gaez_gdal);
     foreach ($result as $record){
       return $record->rs;
     }
     return "NONE";
  } else {
    return "NONE";
  }
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $worldkgeiger_gdal
 */
function get_value_soil_toxic_gaez_from_gdal_value($soil_toxic_gaez_gdal,$way){
  if (strtoupper($way) == "ACCESS_DATABASE"){
     $result = db_query("SELECT soil_toxic_value as rs FROM landpks_gdal_soil_toxic_gaez_lookup WHERE gdal_value = " . $soil_toxic_gaez_gdal);
     foreach ($result as $record){
       return $record->rs;
     }
     return "NONE";
  } else {
    return "NONE";
  }
}


/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $worldkgeiger_gdal
 */
function get_value_cereal_from_gdal_value($cereal_gdal,$way){
  if (strtoupper($way) == "ACCESS_DATABASE"){
     $result = db_query("SELECT cereals_suitability_class as rs FROM landpks_gdal_cereals_suitability_lookup WHERE gdal_value = " . $cereal_gdal);
     foreach ($result as $record){
       return $record->rs;
     }
     return "NONE";
  } else {
    return "NONE";
  }
}


/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $worldkgeiger_gdal
 */
function get_value_soil_depth_gaez_from_gdal_value($soil_depth_gdal,$way){
  if (strtoupper($way) == "ACCESS_DATABASE"){
     $result = db_query("SELECT depth_value as rs FROM landpks_gdal_soil_depth_gaez_lookup WHERE gdal_value = " . $soil_depth_gdal);
     foreach ($result as $record){
       return $record->rs;
     }
     return "NONE";
  } else {
    return "NONE";
  }
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $worldkgeiger_gdal
 */
function get_value_landcover_modis_from_gdal_value($landcover_modis_gdal,$way){
  if (strtoupper($way) == "ACCESS_DATABASE"){
     $result = db_query("SELECT color, name, description, minimum, maximum FROM landpks_gdal_landcover_modis_lookup WHERE gdal_value = " . $landcover_modis_gdal);
     foreach ($result as $record){
       return $record->color . " : " . $record->name . " : " . $record->description . " : " . $record->minimum . " : " . $record->maximum;
     }
     return "NONE";
  } else {
    return "NONE";
  }
}


/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $worldkgeiger_gdal
 */
function get_value_protected_area_from_gdal_value($area_gdal,$way){
  if (strtoupper($way) == "ACCESS_DATABASE"){
     $result = db_query("SELECT protected_area_value as rs FROM landpks_gdal_landcover_protected_areas_lookup WHERE gdal_value = " . $area_gdal);
     foreach ($result as $record){
       return $record->rs;
     }
     return "NONE";
  } else {
    return "NONE";
  }
}

/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $worldkgeiger_gdal
 */
function get_value_protected_agr_area_from_gdal_value($area_gdal,$way){
  if (strtoupper($way) == "ACCESS_DATABASE"){
     $result = db_query("SELECT protected_area_agri_value as rs FROM landpks_gdal_landcover_protect_agri_lookup WHERE gdal_value = " . $area_gdal);
     foreach ($result as $record){
       return $record->rs;
     }
     return "NONE";
  } else {
    return "NONE";
  }
}
/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $record_id
 * @param unknown_type $month
 */
function get_monthly_max_temp_per_month($record_id){
     $result = db_query("SELECT climate_max_temp_jan, climate_max_temp_feb, climate_max_temp_mar, climate_max_temp_apr, climate_max_temp_may, climate_max_temp_jun, climate_max_temp_jul, climate_max_temp_aug, climate_max_temp_sep, climate_max_temp_oct, climate_max_temp_nov, climate_max_temp_dec FROM landpks_climate_max_temp_summary WHERE record_id = $record_id");
     foreach ($result as $record){
       
       $object->climate_max_temp_jan = $record->climate_max_temp_jan;
       $object->climate_max_temp_feb = $record->climate_max_temp_feb;
       $object->climate_max_temp_mar = $record->climate_max_temp_mar;
       $object->climate_max_temp_apr = $record->climate_max_temp_apr;
       $object->climate_max_temp_may = $record->climate_max_temp_may;
       $object->climate_max_temp_jun = $record->climate_max_temp_jun;
       $object->climate_max_temp_jul = $record->climate_max_temp_jul;
       $object->climate_max_temp_aug = $record->climate_max_temp_aug;
       $object->climate_max_temp_sep = $record->climate_max_temp_sep;
       $object->climate_max_temp_oct = $record->climate_max_temp_oct;
       $object->climate_max_temp_nov = $record->climate_max_temp_nov;
       $object->climate_max_temp_dec = $record->climate_max_temp_dec;
       return $object;
     }
     
     return null;
}
/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $record_id
 * @param unknown_type $month
 */
function get_monthly_min_temp_per_month($record_id){
     $result = db_query("SELECT climate_min_temp_jan, climate_min_temp_feb, climate_min_temp_mar, climate_min_temp_apr, climate_min_temp_may, climate_min_temp_jun, climate_min_temp_jul, climate_min_temp_aug, climate_min_temp_sep, climate_min_temp_oct, climate_min_temp_nov, climate_min_temp_dec FROM landpks_climate_min_temp_summary WHERE record_id = $record_id");
     foreach ($result as $record){
       
       $object->climate_min_temp_jan = $record->climate_min_temp_jan;
       $object->climate_min_temp_feb = $record->climate_min_temp_feb;
       $object->climate_min_temp_mar = $record->climate_min_temp_mar;
       $object->climate_min_temp_apr = $record->climate_min_temp_apr;
       $object->climate_min_temp_may = $record->climate_min_temp_may;
       $object->climate_min_temp_jun = $record->climate_min_temp_jun;
       $object->climate_min_temp_jul = $record->climate_min_temp_jul;
       $object->climate_min_temp_aug = $record->climate_min_temp_aug;
       $object->climate_min_temp_sep = $record->climate_min_temp_sep;
       $object->climate_min_temp_oct = $record->climate_min_temp_oct;
       $object->climate_min_temp_nov = $record->climate_min_temp_nov;
       $object->climate_min_temp_dec = $record->climate_min_temp_dec;
       return $object;
     }
     
     return null;
}

/**NGUYEN HAI THANH
 * 
 */
function get_monthly_precipitation_per_month($record_id){
     $result = db_query("SELECT climate_precip_jan, climate_precip_feb, climate_precip_mar, climate_precip_apr, climate_precip_may, climate_precip_jun, climate_precip_jul, climate_precip_aug, climate_precip_sep, climate_precip_oct, climate_precip_nov, climate_precip_dec FROM landpks_climate_precip_summary WHERE record_id = $record_id");
     foreach ($result as $record){
       $object->climate_precip_jan = $record->climate_precip_jan;
       $object->climate_precip_feb = $record->climate_precip_feb;
       $object->climate_precip_mar = $record->climate_precip_mar;
       $object->climate_precip_apr = $record->climate_precip_apr;
       $object->climate_precip_may = $record->climate_precip_may;
       $object->climate_precip_jun = $record->climate_precip_jun;
       $object->climate_precip_jul = $record->climate_precip_jul;
       $object->climate_precip_aug = $record->climate_precip_aug;
       $object->climate_precip_sep = $record->climate_precip_sep;
       $object->climate_precip_oct = $record->climate_precip_oct;
       $object->climate_precip_nov = $record->climate_precip_nov;
       $object->climate_precip_dec = $record->climate_precip_dec;
       $object->climate_precip_annual = floatval($record->climate_precip_jan) + floatval($record->climate_precip_feb) + floatval($record->climate_precip_mar) + floatval($record->climate_precip_apr) + floatval($record->climate_precip_may) + floatval($record->climate_precip_jun) + floatval($record->climate_precip_jul) + floatval($object->climate_precip_aug) + floatval($record->climate_precip_sep) + floatval($record->climate_precip_oct) + floatval($object->climate_precip_nov) + floatval($record->climate_precip_dec);
       return $object;
     }
     
     return null;
}
/**
 * NGUYEN HAI THANH
 * Enter description here ...
 * @param unknown_type $record_id
 */
function get_soil_profile_awc_value_plot($record_id){
  $sql = "SELECT soil_profile_awc as rs FROM landpks_rosetta_awc_output_data WHERE record_id = $record_id";
  $result = db_query($sql);
  foreach ($result as $record){
    return $record->rs;
  }
  return null;
}

/*****************************************************************************************************/
/********************EXPORT PROJECT*******************************************************************/
/*****************************************************************************************************/
function parseName($string){
  $index = stripos($string, "-");
  $string_length = strlen($string);
  return trim(substr($string, $index + 1,$string_length -  $index));
}
/**
 * NGUYEN HAI THANH
 * GET List LandPKS Plot Information via CSV File
 */
function get_list_LandPKS_record_information($record_name){
  $sql = "SELECT ID, name, recorder_name, organization, latitude, longitude, city, modified_date, land_cover, grazed, flooding, slope, slope_shape,";
  $sql .= " rock_fragment_for_soil_horizon_1, rock_fragment_for_soil_horizon_2, rock_fragment_for_soil_horizon_3,rock_fragment_for_soil_horizon_4,";
  $sql .= " rock_fragment_for_soil_horizon_5, rock_fragment_for_soil_horizon_6, rock_fragment_for_soil_horizon_7, color_for_soil_horizon_1, color_for_soil_horizon_2,";
  $sql .= " color_for_soil_horizon_3, color_for_soil_horizon_4, color_for_soil_horizon_5, color_for_soil_horizon_6, color_for_soil_horizon_7, texture_for_soil_horizon_1,";
  $sql .= " texture_for_soil_horizon_2, texture_for_soil_horizon_3, texture_for_soil_horizon_4, texture_for_soil_horizon_5, texture_for_soil_horizon_6, texture_for_soil_horizon_7,";
  $sql .= " surface_cracking, surface_salt, insert_normal_time";
  $sql .= " FROM landpks_input_data";
  $sql .= " WHERE 1 = 1";
  $array_landpks = array();
  
  if (!isEmpty($record_name)){
    $sql .= " AND recorder_name='". $record_name ."'";
  }  
  $sql .= " ORDER BY ID DESC";
  
  $results = db_query($sql);
  
  $i = 0;
  foreach ($results as $record){
    $array_landpks[$i]->ID = $record->ID;
    $array_landpks[$i]->name = parseName($record->name);
    $array_landpks[$i]->recorder_name = $record->recorder_name;
    $array_landpks[$i]->organization = $record->organization;
    $array_landpks[$i]->latitude = $record->latitude;
    $array_landpks[$i]->longitude = $record->longitude;
    $array_landpks[$i]->city = $record->city;
    $array_landpks[$i]->modified_date = $record->modified_date;
    $array_landpks[$i]->land_cover = $record->land_cover;
    $array_landpks[$i]->grazed = $record->grazed;
    $array_landpks[$i]->flooding = $record->flooding;
    $array_landpks[$i]->slope = $record->slope;
    $array_landpks[$i]->slope_shape = $record->slope_shape;
    $array_landpks[$i]->rock_fragment_for_soil_horizon_1 = $record->rock_fragment_for_soil_horizon_1;
    $array_landpks[$i]->rock_fragment_for_soil_horizon_2 = $record->rock_fragment_for_soil_horizon_2;
    $array_landpks[$i]->rock_fragment_for_soil_horizon_3 = $record->rock_fragment_for_soil_horizon_3;
    $array_landpks[$i]->rock_fragment_for_soil_horizon_4 = $record->rock_fragment_for_soil_horizon_4;
    $array_landpks[$i]->rock_fragment_for_soil_horizon_5 = $record->rock_fragment_for_soil_horizon_5;
    $array_landpks[$i]->rock_fragment_for_soil_horizon_6 = $record->rock_fragment_for_soil_horizon_6;
    $array_landpks[$i]->rock_fragment_for_soil_horizon_7 = $record->rock_fragment_for_soil_horizon_7;
    $array_landpks[$i]->color_for_soil_horizon_1 = $record->color_for_soil_horizon_1;
    $array_landpks[$i]->color_for_soil_horizon_2 = $record->color_for_soil_horizon_2;
    $array_landpks[$i]->color_for_soil_horizon_3 = $record->color_for_soil_horizon_3;
    $array_landpks[$i]->color_for_soil_horizon_4 = $record->color_for_soil_horizon_4;
    $array_landpks[$i]->color_for_soil_horizon_5 = $record->color_for_soil_horizon_5;
    $array_landpks[$i]->color_for_soil_horizon_6 = $record->color_for_soil_horizon_6;
    $array_landpks[$i]->color_for_soil_horizon_7 = $record->color_for_soil_horizon_7;
    $array_landpks[$i]->texture_for_soil_horizon_1 = $record->texture_for_soil_horizon_1;
    $array_landpks[$i]->texture_for_soil_horizon_2 = $record->texture_for_soil_horizon_2;
    $array_landpks[$i]->texture_for_soil_horizon_3 = $record->texture_for_soil_horizon_3;
    $array_landpks[$i]->texture_for_soil_horizon_4 = $record->texture_for_soil_horizon_4;
    $array_landpks[$i]->texture_for_soil_horizon_5 = $record->texture_for_soil_horizon_5;
    $array_landpks[$i]->texture_for_soil_horizon_6 = $record->texture_for_soil_horizon_6;
    $array_landpks[$i]->texture_for_soil_horizon_7 = $record->texture_for_soil_horizon_7;
    $array_landpks[$i]->insert_normal_time = $record->insert_normal_time;
    $array_landpks[$i]->surface_cracking = $record->surface_cracking;
    $array_landpks[$i]->surface_salt = $record->surface_salt;
 
    $gdal_object = get_raw_output_data_NO_APEX_output($record->ID);
    $array_landpks[$i]->climate_max_temp_jan = $gdal_object->climate_max_temp_jan;
    $array_landpks[$i]->climate_max_temp_feb = $gdal_object->climate_max_temp_feb;
    $array_landpks[$i]->climate_max_temp_mar = $gdal_object->climate_max_temp_mar;
    $array_landpks[$i]->climate_max_temp_apr = $gdal_object->climate_max_temp_apr;
    $array_landpks[$i]->climate_max_temp_may = $gdal_object->climate_max_temp_may;
    $array_landpks[$i]->climate_max_temp_jun = $gdal_object->climate_max_temp_jun;
    $array_landpks[$i]->climate_max_temp_jul = $gdal_object->climate_max_temp_jul;
    $array_landpks[$i]->climate_max_temp_aug = $gdal_object->climate_max_temp_aug;
    $array_landpks[$i]->climate_max_temp_sep = $gdal_object->climate_max_temp_sep;
    $array_landpks[$i]->climate_max_temp_oct = $gdal_object->climate_max_temp_oct;
    $array_landpks[$i]->climate_max_temp_nov = $gdal_object->climate_max_temp_nov;
    $array_landpks[$i]->climate_max_temp_dec = $gdal_object->climate_max_temp_dec;
    
    $array_landpks[$i]->climate_min_temp_jan = $gdal_object->climate_min_temp_jan;
    $array_landpks[$i]->climate_min_temp_feb = $gdal_object->climate_min_temp_feb;
    $array_landpks[$i]->climate_min_temp_mar = $gdal_object->climate_min_temp_mar;
    $array_landpks[$i]->climate_min_temp_apr = $gdal_object->climate_min_temp_apr;
    $array_landpks[$i]->climate_min_temp_may = $gdal_object->climate_min_temp_may;
    $array_landpks[$i]->climate_min_temp_jun = $gdal_object->climate_min_temp_jun;
    $array_landpks[$i]->climate_min_temp_jul = $gdal_object->climate_min_temp_jul;
    $array_landpks[$i]->climate_min_temp_aug = $gdal_object->climate_min_temp_aug;
    $array_landpks[$i]->climate_min_temp_sep = $gdal_object->climate_min_temp_sep;
    $array_landpks[$i]->climate_min_temp_oct = $gdal_object->climate_min_temp_oct;
    $array_landpks[$i]->climate_min_temp_nov = $gdal_object->climate_min_temp_nov;
    $array_landpks[$i]->climate_min_temp_dec = $gdal_object->climate_min_temp_dec;
    
    $array_landpks[$i]->climate_precip_jan = $gdal_object->climate_precip_jan;
    $array_landpks[$i]->climate_precip_feb = $gdal_object->climate_precip_feb;
    $array_landpks[$i]->climate_precip_mar = $gdal_object->climate_precip_mar;
    $array_landpks[$i]->climate_precip_apr = $gdal_object->climate_precip_apr;
    $array_landpks[$i]->climate_precip_may = $gdal_object->climate_precip_may;
    $array_landpks[$i]->climate_precip_jun = $gdal_object->climate_precip_jun;
    $array_landpks[$i]->climate_precip_jul = $gdal_object->climate_precip_jul;
    $array_landpks[$i]->climate_precip_aug = $gdal_object->climate_precip_aug;
    $array_landpks[$i]->climate_precip_sep = $gdal_object->climate_precip_sep;
    $array_landpks[$i]->climate_precip_oct = $gdal_object->climate_precip_oct;
    $array_landpks[$i]->climate_precip_nov = $gdal_object->climate_precip_nov;
    $array_landpks[$i]->climate_precip_dec = $gdal_object->climate_precip_dec;
    $array_landpks[$i]->climate_precip_annual = $gdal_object->climate_precip_annual;
    
    $array_landpks[$i]->soil_profile_awc = $gdal_object->soil_profile_awc;
    $array_landpks[$i]->old_elevation = $gdal_object->old_elevation;
    $array_landpks[$i]->fao_lgp_value = $gdal_object->fao_lgp;
    $array_landpks[$i]->aridity = $gdal_object->aridity;
    
    $i++;
  }
  if ($i <> 0){
    return $array_landpks;
  } else {
    return false;
  }
}

/*
 * NGUYEN HAI THANH
 * GET List RHM Plot information via CSV file
 */
function get_list_RHM_record_information($record_name){
  $sql = "SELECT ID, name, recorder_name, transect, segment, date, canopy_height, canopy_gap, basal_gap, species_1_density, species_2_density, species_list,";
  $sql .= " stick_segment_0, stick_segment_1, stick_segment_2, stick_segment_3, stick_segment_4, bare_total, trees_total, shrubs_total, sub_shrubs_total,";
  $sql .= " perennial_grasses_total, annuals_total, herb_litter_total, wood_litter_total, rock_total";
  $sql .= " FROM rhm_input_data";
  $sql .= " WHERE 1 = 1";
  $array_rhm = array();
  
  if (!isEmpty($record_name)){
    $sql .= " AND recorder_name='". $record_name ."'";
  }  
  $sql .= " ORDER BY ID DESC";
  
  $results = db_query($sql);
  $i = 0 ;
  $old_name = "";
  foreach ($results as $record){
    $array_rhm[$i]->ID = $record->ID;
    $new_name = $record->name;
    $array_rhm[$i]->name =  parseName($record->name);
    $array_rhm[$i]->recorder_name = $record->recorder_name;
    $array_rhm[$i]->transect = $record->transect;
    $array_rhm[$i]->segment = $record->segment;
    $array_rhm[$i]->date = $record->date;
    $array_rhm[$i]->canopy_height = $record->canopy_height;
    $array_rhm[$i]->canopy_gap = $record->canopy_gap;
    $array_rhm[$i]->basal_gap = $record->basal_gap;
    $array_rhm[$i]->species_1_density = $record->species_1_density;
    $array_rhm[$i]->species_2_density = $record->species_2_density;
    $array_rhm[$i]->species_list = $record->species_list;
    $array_rhm[$i]->stick_segment_0 = $record->stick_segment_0;
    $array_rhm[$i]->stick_segment_1 = $record->stick_segment_1;
    $array_rhm[$i]->stick_segment_2 = $record->stick_segment_2;
    $array_rhm[$i]->stick_segment_3 = $record->stick_segment_3;
    $array_rhm[$i]->stick_segment_4 = $record->stick_segment_4;
    $array_rhm[$i]->bare_total = $record->bare_total;
    $array_rhm[$i]->trees_total = $record->trees_total;
    $array_rhm[$i]->shrubs_total = (int)($record->shrubs_total) - (int)($record->sub_shrubs_total);
    $array_rhm[$i]->sub_shrubs_total = $record->sub_shrubs_total;
    $array_rhm[$i]->perennial_grasses_total = $record->perennial_grasses_total;
    $array_rhm[$i]->annuals_total = $record->annuals_total;
    $array_rhm[$i]->herb_litter_total = $record->herb_litter_total;
    $array_rhm[$i]->wood_litter_total = $record->wood_litter_total;
    $array_rhm[$i]->rock_total = $record->rock_total;
    
    /* Calculate Summary data from group by name */
    if ($new_name <> $old_name){
        /* Calculate Summary data from group by name */
        $objects = get_output_value_RHM_record($new_name);
        $old_name = $new_name;
        
        /* Binding to records */
        $array_rhm[$i]->bare_ground_1_percent = $objects->bare_ground_1_percent;
        $array_rhm[$i]->veg_cover_percent = $objects->veg_cover_percent;
       
        $array_rhm[$i]->bare_ground_2 = $objects->bare_ground_2;
        $array_rhm[$i]->perennial_grasses = $objects->perennial_grasses;
        $array_rhm[$i]->tree = $objects->tree;
        $array_rhm[$i]->shrubs = (int)($objects->shrubs) - (int)($objects->sub_shrubs);
        $array_rhm[$i]->sub_shrubs = $objects->sub_shrubs;
        $array_rhm[$i]->annual = $objects->annual;
        $array_rhm[$i]->herb_litter = $objects->herb_litter;
        $array_rhm[$i]->wood_litter = $objects->wood_litter;
        $array_rhm[$i]->rock = $objects->rock;
        $array_rhm[$i]->foliar_cover = (int)($array_rhm[$i]->tree) + (int)($array_rhm[$i]->shrubs) + (int)($array_rhm[$i]->sub_shrubs) + (int)($array_rhm[$i]->annual) + (int)($array_rhm[$i]->perennial_grasses);
        
        $array_rhm[$i]->canopy_gap_percent = $objects->canopy_gap_percent;
        $array_rhm[$i]->basal_gap_percent = $objects->basal_gap_percent;
  
        $array_rhm[$i]->species_1_density_percent = $objects->species_1_density_percent;
        $array_rhm[$i]->species_2_density_percent = $objects->species_2_density_percent;
        
        $array_rhm[$i]->canopy_height_smaller_10_cm = $objects->canopy_height_smaller_10_cm;
        $array_rhm[$i]->canopy_height_10_50_cm = $objects->canopy_height_10_50_cm;
        $array_rhm[$i]->canopy_height_50cm_1m = $objects->canopy_height_50cm_1m;
        $array_rhm[$i]->canopy_height_1m_2m = $objects->canopy_height_1m_2m;
        $array_rhm[$i]->canopy_height_2m_3m = $objects->canopy_height_2m_3m;
        $array_rhm[$i]->canopy_height_greater_3m = $objects->canopy_height_greater_3m;
        
        //$result_inser_output = insert_rhm_output_data($record->ID,$new_name, $objects);
        
    } else {
        /* Binding to records */
		/*
        $array_rhm[$i]->bare_ground_1_percent = $objects->bare_ground_1_percent;
        $array_rhm[$i]->veg_cover_percent = $objects->veg_cover_percent;
       
        $array_rhm[$i]->bare_ground_2 = $objects->bare_ground_2;
        $array_rhm[$i]->perennial_grasses = $objects->perennial_grasses;
        $array_rhm[$i]->tree = $objects->tree;
        $array_rhm[$i]->shrubs = (int)($objects->shrubs) - (int)($objects->sub_shrubs);
        $array_rhm[$i]->sub_shrubs = $objects->sub_shrubs;
        $array_rhm[$i]->annual = $objects->annual;
        $array_rhm[$i]->herb_litter = $objects->herb_litter;
        $array_rhm[$i]->wood_litter = $objects->wood_litter;
        $array_rhm[$i]->rock = $objects->rock;
        $array_rhm[$i]->foliar_cover = (int)($array_rhm[$i]->tree) + (int)($array_rhm[$i]->shrubs) + (int)($array_rhm[$i]->sub_shrubs) + (int)($array_rhm[$i]->annual) + (int)($array_rhm[$i]->perennial_grasses);
        
        $array_rhm[$i]->canopy_gap_percent = $objects->canopy_gap_percent;
        $array_rhm[$i]->basal_gap_percent = $objects->basal_gap_percent;
  
        $array_rhm[$i]->species_1_density_percent = $objects->species_1_density_percent;
        $array_rhm[$i]->species_2_density_percent = $objects->species_2_density_percent;
        
        $array_rhm[$i]->canopy_height_smaller_10_cm = $objects->canopy_height_smaller_10_cm;
        $array_rhm[$i]->canopy_height_10_50_cm = $objects->canopy_height_10_50_cm;
        $array_rhm[$i]->canopy_height_50cm_1m = $objects->canopy_height_50cm_1m;
        $array_rhm[$i]->canopy_height_1m_2m = $objects->canopy_height_1m_2m;
        $array_rhm[$i]->canopy_height_2m_3m = $objects->canopy_height_2m_3m;
        $array_rhm[$i]->canopy_height_greater_3m = $objects->canopy_height_greater_3m;
		*/
		$array_rhm[$i]->bare_ground_1_percent = "";
        $array_rhm[$i]->veg_cover_percent = "";
       
        $array_rhm[$i]->bare_ground_2 = "";
        $array_rhm[$i]->perennial_grasses = "";
        $array_rhm[$i]->tree = "";
        $array_rhm[$i]->shrubs = "";
        $array_rhm[$i]->sub_shrubs = "";
        $array_rhm[$i]->annual = "";
        $array_rhm[$i]->herb_litter = "";
        $array_rhm[$i]->wood_litter = "";
        $array_rhm[$i]->rock = "";
        $array_rhm[$i]->foliar_cover = "";
        
        $array_rhm[$i]->canopy_gap_percent = "";
        $array_rhm[$i]->basal_gap_percent = "";
  
        $array_rhm[$i]->species_1_density_percent = "";
        $array_rhm[$i]->species_2_density_percent = "";
        
        $array_rhm[$i]->canopy_height_smaller_10_cm = "";
        $array_rhm[$i]->canopy_height_10_50_cm = "";
        $array_rhm[$i]->canopy_height_50cm_1m = "";
        $array_rhm[$i]->canopy_height_1m_2m = "";
        $array_rhm[$i]->canopy_height_2m_3m = "";
        $array_rhm[$i]->canopy_height_greater_3m = "";
    }
    

    $i++;
  }
  if ($i <> 0){
    return $array_rhm;
  } else {
    return false;
  }
}


function save_to_csv_file($data,$path){
  global $base_url;
  global $user;
  $name = $user->uid ."-" . $user->name . "-" . time() . ".csv";
  $fp = fopen("sites/default/public_shiny_csv/$name", 'w');
  fputcsv($fp, array(
       'name','recorder_name','transect','segment','date','canopy_height','canopy_gap','basal_gap','species_1_density','species_2_density','species_list',
       'stick_segment_0','stick_segment_1','stick_segment_2','stick_segment_3','stick_segment_4','bare_total','trees_total','shrubs_total','sub_shrubs_total',
       'perennial_grasses_total','annuals_total','herb_litter_total','wood_litter_total','rock_total' 
    ));
  foreach ($data as $job) {
        fputcsv($fp,array($job->name,$job->recorder_name,$job->transect,$job->segment,$job->date,$job->canopy_height,$job->canopy_gap,$job->basal_gap,
                              $job->species_1_density,$job->species_2_density,$job->species_list,$job->stick_segment_0,$job->stick_segment_1,$job->stick_segment_2,
                              $job->stick_segment_3,$job->stick_segment_4, $job->bare_total, $job->trees_total,$job->shrubs_total,$job->sub_shrubs_total,$job->perennial_grasses_total,
                              $job->annuals_total,$job->herb_litter_total,$job->wood_litter_total,$job->rock_total
                         )
                );
  }
  fclose($fp);
  return $base_url . "/sites/default/public_shiny_csv/$name";
}
?>