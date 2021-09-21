<?php
    $data = $_POST['data'];
    $term = $data[1];
    $path = $data[0];

    $path_parts = explode("\\", $path);
    $old_name = $path_parts[sizeof($path_parts)-1];
    $new_name = trim($term)."-".$old_name;

    $new_path = "";
    for($i = 0; $i < sizeof($path_parts)-1; $i++){
        $new_path = $new_path.$path_parts[$i]."\\";
    }
    $new_path = $new_path.$new_name;

    $result = rename($path, $new_path);
    echo $result;
?>