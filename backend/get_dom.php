<?php
// Enable error reporting for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Set default URL (fallback)
$url = "https://usindh.edu.pk";

// Check if the URL parameter is provided
if (isset($_GET["url"])) {
    $url = filter_var($_GET["url"], FILTER_SANITIZE_URL);
}

// Validate the URL format
if (!filter_var($url, FILTER_VALIDATE_URL)) {
    die("Invalid URL format");
}

// Write the URL to the input file
$inputFile = 'read_write/input.txt';
if (!is_dir('read_write')) {
    mkdir('read_write', 0777, true); // Create the directory if it doesn't exist
}

$file = fopen($inputFile, 'w') or die("Unable to open file for writing!");
fwrite($file, $url);
fclose($file);

// Output the URL for confirmation/debugging
echo "Processing URL: " . htmlspecialchars($url) . "<br>";

// Execute the Python script
$pythonScript = 'ACI_Main.py';
$pythonCommand = escapeshellcmd("python3.6 $pythonScript 2>&1");
exec($pythonCommand, $output, $err);

// Check for errors in the execution
if ($err !== 0) {
    echo "Python script execution failed!<br>";
    echo "<pre>Error Details:\n";
    print_r($output);
    echo "</pre>";
    die("Execution stopped due to an error.");
}

// Output success message and Python script output
echo "Python script executed successfully!<br>";
echo "<pre>Output:\n";
print_r($output);
echo "</pre>";

?>
