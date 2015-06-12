<?php
function parseToXML($htmlStr)
{
  $xmlStr=str_replace('<','&lt;',$htmlStr);
  $xmlStr=str_replace('>','&gt;',$xmlStr);
  $xmlStr=str_replace('"','&quot;',$xmlStr);
  $xmlStr=str_replace("'",'&#39;',$xmlStr);
  $xmlStr=str_replace("&",'&amp;',$xmlStr);
  return $xmlStr;
}
function parseName($string){
  $index = stripos($string, "-");
  $string_length = strlen($string);
  return trim(substr($string, $index + 1,$string_length -  $index));
}
?>
