// Global Variables
var g_filesRead = 0;
var g_Text, g_Keywords, g_Score, g_Tokens, g_Stopwords, g_Lemma, g_Stemm, g_POS;

// Initialize Process
function onStart() {
  document.getElementById("buttons_section").style.display = "none";
  document.getElementById("output_section").style.display = "none";
  document.getElementById("progress_section").style.display = "block";
  document.getElementById("msg").innerText = "Loading...";
  move();
  extractKeywords();
}

// Extract Keywords
function extractKeywords() {
  var url = document.getElementById("input_url").value.trim();
  if (url !== "") {
    if (!url.startsWith("https://")) {
      url = "https://" + url;
    }
  }
  var request = "https://cs.uef.fi/~himat/ACI/get_dom.php?url=" + url;
  g_filesRead = 0; // Reset file counter
  sendRequest(request, onExtractionReady);
}

// Check Files Ready
function checkFilesReady() {
  if (g_filesRead === 8) {
    document.getElementById("progress_section").style.display = "none";
    document.getElementById("buttons_section").style.display = "block";
    document.getElementById("output_section").style.display = "block";
    document.getElementById("msg").innerHTML = "<h1><b>Loading finished</b></h1>";
  }
}

// Progress Bar Animation
function move() {
  var elem = document.getElementById("progress_bar_3");
  var width = 0;
  var intervalId = setInterval(() => {
    if (g_filesRead === 8) {
      clearInterval(intervalId);
    } else if (width < 100) {
      width++;
      elem.style.width = width + "%";
    }
  }, 50);
}

// Send HTTP Request
function sendRequest(request, callback) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", request, true);
  xhr.send();
  xhr.onreadystatechange = () => {
    if (xhr.readyState === 4 && xhr.status === 200) {
      callback(xhr.response);
    }
  };
}

// Handle Extraction Ready Event
function onExtractionReady() {
  readText();
  readScore();
  readKeywords();
  readTokens();
  readStopwords();
  readLemma();
  readStemm();
  readPOS();
}

// Read and Display Functions
function readText() {
  var request = "https://cs.uef.fi/~himat/ACI/read_write/text.txt?rand=" + Math.random();
  sendRequest(request, onTextReady);
}
function onTextReady(fileContents) {
  g_Text = fileContents;
  g_filesRead++;
  checkFilesReady();
}
function showText() {
  document.getElementById("output_content").innerHTML = g_Text;
}

function readScore() {
  var request = "https://cs.uef.fi/~himat/ACI/read_write/feature.txt?rand=" + Math.random();
  sendRequest(request, onScoreReady);
}
function onScoreReady(fileContents) {
  g_Score = fileContents;
  g_filesRead++;
  checkFilesReady();
}
function showScore() {
  document.getElementById("output_content").innerText = g_Score;
}

function readKeywords() {
  var request = "https://cs.uef.fi/~himat/ACI/read_write/keyphrase.txt?rand=" + Math.random();
  sendRequest(request, onKeywordsReady);
}
function onKeywordsReady(fileContents) {
  g_Keywords = fileContents;
  g_filesRead++;
  checkFilesReady();
}
function showKeywords() {
  document.getElementById("output_content").innerHTML = g_Keywords;
}

function readTokens() {
  var request = "https://cs.uef.fi/~himat/ACI/read_write/tokens.txt?rand=" + Math.random();
  sendRequest(request, onTokensReady);
}
function onTokensReady(fileContents) {
  g_Tokens = fileContents;
  g_filesRead++;
  checkFilesReady();
}
function showTokens() {
  document.getElementById("output_content").innerHTML = g_Tokens;
}

function readStopwords() {
  var request = "https://cs.uef.fi/~himat/ACI/read_write/stopwords.txt?rand=" + Math.random();
  sendRequest(request, onStopwordsReady);
}
function onStopwordsReady(fileContents) {
  g_Stopwords = fileContents;
  g_filesRead++;
  checkFilesReady();
}
function showStopwords() {
  document.getElementById("output_content").innerHTML = g_Stopwords;
}

function readLemma() {
  var request = "https://cs.uef.fi/~himat/ACI/read_write/lemma.txt?rand=" + Math.random();
  sendRequest(request, onLemmaReady);
}
function onLemmaReady(fileContents) {
  g_Lemma = fileContents;
  g_filesRead++;
  checkFilesReady();
}
function showLemma() {
  document.getElementById("output_content").innerHTML = g_Lemma;
}

function readStemm() {
  var request = "https://cs.uef.fi/~himat/ACI/read_write/stemm.txt?rand=" + Math.random();
  sendRequest(request, onStemmReady);
}
function onStemmReady(fileContents) {
  g_Stemm = fileContents;
  g_filesRead++;
  checkFilesReady();
}
function showStemm() {
  document.getElementById("output_content").innerHTML = g_Stemm;
}

function readPOS() {
  var request = "https://cs.uef.fi/~himat/ACI/read_write/pos.txt?rand=" + Math.random();
  sendRequest(request, onPOSReady);
}
function onPOSReady(fileContents) {
  g_POS = fileContents;
  g_filesRead++;
  checkFilesReady();
}
function showPOS() {
  document.getElementById("output_content").innerHTML = g_POS;
}
