var areaNames = ['AK COIL PROCESSING', 'AUCKLAND CENTRAL', 'AUCKLAND EAST', 'AUCKLAND NORTH', 'AUCKLAND SOUTH', 'AUCKLAND WEST', 'CENTRAL OTAGO', 'CH COIL PROCESSING', 'CHCH EAST', 'CHCH NORTH', 'CHCH SOUTH', 'CHCH WEST', 'COROMANDEL', 'DUNEDIN OTAGO', 'GISBORNE', 'HAMILTON', 'HAWKES BAY', 'KATIKATI TO PAEROA', 'LEVIN', 'MARLBOROUGH', 'MATAMATA-TIRAU', 'MERCHANT NORTH ISLAN', 'MERCHANT SOUTH ISLAN', 'MID CANTERBURY', 'MOUNT - TEPUKE', 'NELSON & BAYS', 'NORTH CANTERBURY', 'NORTH OTAGO', 'NORTHLAND', 'PALMERSTON NORTH', 'ROTORUA', 'SOUTH CANTERBURY', 'SOUTH OTAGO', 'SOUTHLAND', 'STAINLESS', 'TARANAKI', 'TAUPO-TURANGI', 'TAURANGA', 'TOKOROA-PUTARURU', 'WAIKATO', 'WAIRARAPA DISTRICT', 'WANGANUI', 'WELLINGTON', 'WEST COAST', 'WHAK-KAWER-OPOTIKI'];

var industryNames = ['DAIRY INDUSTRY', 'DAIRY SHEDS', 'DOOR MANUFACTURER', 'FENCING', 'FOOD MANUFACTURERS', 'GENERAL ENGINEERING', 'MANUFACTURERS', 'MARINE INDUSTRY', 'MATERIALS HANDLING', 'PROJECT ENGINEERS', 'RESELLER/COMPETITOR', 'ROLLFORMERS', 'Re-Work', 'SHEETMETAL ENGINEERS', 'STAINLESS STEEL FAB', 'STEEL FABRICATORS', 'STRUCTURAL CONSTRUCTION', 'TRAINING INSTITUTE', 'TRANSPORT ENGINEERS', 'UNDEFINED'];

// Populate areaName select menu
var areaNameSelect = document.getElementById("areaName");
for (var i = 0; i < areaNames.length; i++) {
  var option = document.createElement("option");
  option.value = areaNames[i];
  option.text = areaNames[i];
  areaNameSelect.appendChild(option);
}

    // Populate industryName select menu
var industryNameSelect = document.getElementById("industryName");
for (var i = 0; i < industryNames.length; i++) {
  var option = document.createElement("option");
  option.value = industryNames[i];
  option.text = industryNames[i];
  industryNameSelect.appendChild(option);
}

  

 function getRecommendations() {
  var customerId = document.getElementById("customerId").value;
  var areaName = document.getElementById("areaName").value;
  var industryName = document.getElementById("industryName").value;

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var response = JSON.parse(xhr.responseText);
      displayRecommendations(response);
    }
  };
  xhr.open("GET", "recommendations?customerId=" + encodeURIComponent(customerId) + "&areaName=" + encodeURIComponent(areaName) + "&industryName=" + encodeURIComponent(industryName), true);
  xhr.send();
}

function displayRecommendations(response) {
  var resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "";

  if (response.error) {
    resultDiv.innerHTML = "<p>" + response.error + "</p>";
  } else {
    resultDiv.innerHTML = "<h3>Recommended Products:</h3>";
    var productList = response.products;
    for (var i = 0; i < productList.length; i++) {
      var productName = productList[i];
      resultDiv.innerHTML += "<div class='product-box'><p class='product-name'>" + productName + "</p></div>";
    }
  }
}

document.getElementById("customer-form").addEventListener("submit", getRecommendations());

