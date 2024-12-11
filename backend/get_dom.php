<?php
if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    $url = isset($_GET['url']) ? $_GET['url'] : '';
    
    if (empty($url)) {
        echo "No URL provided.";
        exit;
    }

    $file = fopen('read_write/input.txt', 'w');
    fwrite($file, $url);
    fclose($file);

    exec('python3 ACI.py 2>&1', $output, $return_var);
    if ($return_var !== 0) {
        echo "Error running Python script.";
        print_r($output);
    } else {
        echo implode("\n", $output);
    }
}
?>
