// ============================================================
// RE-VOLT AI - FRONTEND JAVASCRIPT
// ============================================================


// ============================================================
// API URL
// ============================================================

const API_URL = "https://battery-i3ax.onrender.com";


// ============================================================
// GET HTML ELEMENTS
// ============================================================

const demoBtn = document.getElementById("demoBtn");
const analyzeBtn = document.getElementById("analyzeBtn");
const resetBtn = document.getElementById("resetBtn");

const voltageInput = document.getElementById("voltage");
const temperatureInput = document.getElementById("temperature");
const ratedCapacityInput = document.getElementById("ratedCapacity");
const measuredCapacityInput = document.getElementById("measuredCapacity");
const cyclesInput = document.getElementById("cycles");
const resistanceInput = document.getElementById("resistance");

const sohValue = document.getElementById("sohValue");
const conditionBadge = document.getElementById("conditionBadge");

const recommendationText =
    document.getElementById("recommendationText");

const applicationsList =
    document.getElementById("applicationsList");

const warningBox =
    document.getElementById("warningBox");

const warningText =
    document.getElementById("warningText");


// ============================================================
// DEMO DATA
// ============================================================

demoBtn.addEventListener("click", function () {

    voltageInput.value = "3.82";

    temperatureInput.value = "31";

    ratedCapacityInput.value = "4.0";

    measuredCapacityInput.value = "3.4";

    cyclesInput.value = "650";

    resistanceInput.value = "42";

});


// ============================================================
// ANALYZE BATTERY
// ============================================================

analyzeBtn.addEventListener("click", async function () {

    // --------------------------------------------------------
    // Read values from HTML
    // --------------------------------------------------------

    const voltage =
        parseFloat(voltageInput.value);

    const temperature =
        parseFloat(temperatureInput.value);

    const ratedCapacity =
        parseFloat(ratedCapacityInput.value);

    const measuredCapacity =
        parseFloat(measuredCapacityInput.value);

    const cycles =
        parseFloat(cyclesInput.value);

    const resistance =
        parseFloat(resistanceInput.value);


    // --------------------------------------------------------
    // Validate input
    // --------------------------------------------------------

    if (
        isNaN(voltage) ||
        isNaN(temperature) ||
        isNaN(ratedCapacity) ||
        isNaN(measuredCapacity) ||
        isNaN(cycles) ||
        isNaN(resistance)
    ) {

        alert("Please enter all battery values.");

        return;
    }


    // --------------------------------------------------------
    // Check capacity
    // --------------------------------------------------------

    if (measuredCapacity > ratedCapacity) {

        alert(
            "Measured capacity cannot be greater than rated capacity."
        );

        return;
    }


    // --------------------------------------------------------
    // Show loading state
    // --------------------------------------------------------

    analyzeBtn.disabled = true;

    analyzeBtn.textContent = "Analyzing...";

    sohValue.textContent = "--";

    conditionBadge.textContent = "ANALYZING";


    // Hide previous warning

    warningBox.style.display = "none";


    try {

        // ====================================================
        // SEND DATA TO FLASK API
        // ====================================================

        const response = await fetch(
            `${API_URL}/predict`,
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    voltage: voltage,

                    temperature: temperature,

                    // Flask expects "capacity"
                    capacity: measuredCapacity,

                    cycles: cycles,

                    resistance: resistance

                })

            }
        );


        // ====================================================
        // CHECK API RESPONSE
        // ====================================================

        const result = await response.json();


        if (!response.ok) {

            throw new Error(
                result.error ||
                "Prediction failed."
            );

        }


        // ====================================================
        // DISPLAY SOH
        // ====================================================

        sohValue.textContent =
            `${result.soh}%`;


        // ====================================================
        // DISPLAY CONDITION
        // ====================================================

        conditionBadge.textContent =
            result.condition;


        // ====================================================
        // DISPLAY RECOMMENDATION
        // ====================================================

        recommendationText.textContent =
            result.recommendation;


        // ====================================================
        // DISPLAY APPLICATIONS
        // ====================================================

        applicationsList.innerHTML = "";


        result.applications.forEach(function (application) {

            const li =
                document.createElement("li");

            li.textContent =
                application;

            applicationsList.appendChild(li);

        });


        // ====================================================
        // DISPLAY WARNING
        // ====================================================

        if (result.warning) {

            warningText.textContent =
                result.warning;

            warningBox.style.display = "block";

        } else {

            warningBox.style.display = "none";

        }


    } catch (error) {

        console.error(error);

        alert(
            "Unable to connect to the RE-VOLT AI server.\n\n" +
            error.message
        );

        sohValue.textContent = "--";

        conditionBadge.textContent = "ERROR";

    }


    // --------------------------------------------------------
    // Restore button
    // --------------------------------------------------------

    analyzeBtn.disabled = false;

    analyzeBtn.textContent = "Analyze Battery";

});


// ============================================================
// RESET
// ============================================================

resetBtn.addEventListener("click", function () {

    voltageInput.value = "";

    temperatureInput.value = "";

    ratedCapacityInput.value = "";

    measuredCapacityInput.value = "";

    cyclesInput.value = "";

    resistanceInput.value = "";


    sohValue.textContent = "--";

    conditionBadge.textContent = "--";


    recommendationText.textContent =
        "Enter battery information and analyze the battery.";


    applicationsList.innerHTML = "";


    warningBox.style.display = "none";

});
