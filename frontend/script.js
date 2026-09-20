const form = document.getElementById("batteryForm");

const resultSection = document.getElementById("resultSection");

const demoBtn = document.getElementById("demoBtn");

const resetBtn = document.getElementById("resetBtn");

const sohValue = document.getElementById("sohValue");

const sohProgress = document.getElementById("sohProgress");

const conditionBadge =
    document.getElementById("conditionBadge");

const recommendationTitle =
    document.getElementById("recommendationTitle");

const recommendationText =
    document.getElementById("recommendationText");

const applicationList =
    document.getElementById("applicationList");

const warningBox =
    document.getElementById("warningBox");

const warningText =
    document.getElementById("warningText");
const API_URL = "https://battery-i3ax.onrender.com";

/* --------------------------------
   DEMO DATA
-------------------------------- */

demoBtn.addEventListener("click", function () {

    document.getElementById("voltage").value = "3.82";

    document.getElementById("temperature").value = "31";

    document.getElementById("ratedCapacity").value = "4.0";

    document.getElementById("measuredCapacity").value = "3.4";

    document.getElementById("cycles").value = "650";

    document.getElementById("resistance").value = "42";

});


/* --------------------------------
   BATTERY ANALYSIS
-------------------------------- */

form.addEventListener("submit", function (event) {

    event.preventDefault();


    /* GET INPUT VALUES */

    const voltage =
        Number(document.getElementById("voltage").value);

    const temperature =
        Number(document.getElementById("temperature").value);

    const ratedCapacity =
        Number(document.getElementById("ratedCapacity").value);

    const measuredCapacity =
        Number(document.getElementById("measuredCapacity").value);

    const cycles =
        Number(document.getElementById("cycles").value);

    const resistance =
        Number(document.getElementById("resistance").value);


    /* VALIDATION */

    if (
        !Number.isFinite(voltage) ||
        !Number.isFinite(temperature) ||
        !Number.isFinite(ratedCapacity) ||
        !Number.isFinite(measuredCapacity) ||
        !Number.isFinite(cycles) ||
        !Number.isFinite(resistance)
    ) {

        alert("Please enter valid values.");

        return;
    }


    if (ratedCapacity <= 0) {

        alert("Rated capacity must be greater than zero.");

        return;
    }


    if (measuredCapacity < 0) {

        alert("Measured capacity cannot be negative.");

        return;
    }


    if (measuredCapacity > ratedCapacity) {

        alert(
            "Measured capacity cannot be greater than rated capacity."
        );

        return;
    }


    /* --------------------------------
       CAPACITY SOH
    -------------------------------- */

    let capacitySOH =
        (measuredCapacity / ratedCapacity) * 100;


    capacitySOH =
        Math.min(100, Math.max(0, capacitySOH));


    /* --------------------------------
       CYCLE SCORE
    -------------------------------- */

    let cycleScore;

    if (cycles <= 300) {

        cycleScore = 100;

    } else if (cycles <= 600) {

        cycleScore = 90;

    } else if (cycles <= 1000) {

        cycleScore = 75;

    } else if (cycles <= 1500) {

        cycleScore = 60;

    } else {

        cycleScore = 40;

    }


    /* --------------------------------
       RESISTANCE SCORE
    -------------------------------- */

    let resistanceScore;

    if (resistance <= 30) {

        resistanceScore = 100;

    } else if (resistance <= 50) {

        resistanceScore = 90;

    } else if (resistance <= 80) {

        resistanceScore = 70;

    } else if (resistance <= 120) {

        resistanceScore = 50;

    } else {

        resistanceScore = 30;

    }


    /* --------------------------------
       TEMPERATURE SCORE
    -------------------------------- */

    let temperatureScore;

    if (temperature >= 15 && temperature <= 35) {

        temperatureScore = 100;

    } else if (
        temperature > 35 &&
        temperature <= 45
    ) {

        temperatureScore = 75;

    } else if (
        temperature > 45 &&
        temperature <= 55
    ) {

        temperatureScore = 50;

    } else {

        temperatureScore = 20;

    }


    /* --------------------------------
       FINAL SOH
    -------------------------------- */

    let soh =
        capacitySOH * 0.55 +
        cycleScore * 0.15 +
        resistanceScore * 0.20 +
        temperatureScore * 0.10;


    soh =
        Math.round(
            Math.min(100, Math.max(0, soh))
        );


    /* --------------------------------
       CONDITION
    -------------------------------- */

    let condition;

    if (
        soh >= 80 &&
        temperature <= 45 &&
        resistance <= 80
    ) {

        condition = "REUSE";

    } else if (
        soh >= 60 &&
        temperature <= 50 &&
        resistance <= 120
    ) {

        condition = "SECOND LIFE";

    } else if (
        soh >= 40
    ) {

        condition = "FURTHER TESTING";

    } else {

        condition = "RECYCLE";

    }


    /* --------------------------------
       UPDATE SOH
    -------------------------------- */

    sohValue.textContent = soh;

    setTimeout(function () {

        sohProgress.style.width = soh + "%";

    }, 100);


    /* --------------------------------
       CONDITION BADGE
    -------------------------------- */

    conditionBadge.textContent = condition;


    /* --------------------------------
       RECOMMENDATION
    -------------------------------- */

    if (condition === "REUSE") {

        recommendationTitle.textContent =
            "Continue Use";

        recommendationText.textContent =
            "The prototype assessment indicates relatively strong battery health. Further professional electrical and safety testing is required before continued deployment.";

        showApplications([
            "EV / Mobility",
            "High-demand applications",
            "Energy storage"
        ]);

    }


    else if (condition === "SECOND LIFE") {

        recommendationTitle.textContent =
            "Repurpose for Second Life";

        recommendationText.textContent =
            "The battery may be suitable for lower-demand applications after proper testing, cell matching, BMS verification and safety assessment.";

        showApplications([
            "Solar Energy Storage",
            "Backup Power",
            "Telecom Backup",
            "Street Lighting",
            "Microgrid Storage"
        ]);

    }


    else if (condition === "FURTHER TESTING") {

        recommendationTitle.textContent =
            "Additional Testing Required";

        recommendationText.textContent =
            "The current measurements are not sufficient to confidently assign a reuse pathway. Perform additional capacity, resistance, cell-balance and safety testing.";

        showApplications([
            "Diagnostic Testing",
            "Cell-Level Assessment"
        ]);

    }


    else {

        recommendationTitle.textContent =
            "Route Toward Recycling";

        recommendationText.textContent =
            "The prototype assessment indicates poor condition. The battery should undergo professional end-of-life evaluation and appropriate recycling procedures.";

        showApplications([
            "Material Recovery",
            "Battery Recycling"
        ]);

    }


    /* --------------------------------
       SUMMARY
    -------------------------------- */

    document.getElementById("resultVoltage")
        .textContent =
        voltage.toFixed(2) + " V";

    document.getElementById("resultTemperature")
        .textContent =
        temperature.toFixed(1) + " °C";

    document.getElementById("resultCapacity")
        .textContent =
        measuredCapacity.toFixed(2)
        + " / "
        + ratedCapacity.toFixed(2)
        + " Ah";

    document.getElementById("resultCycles")
        .textContent =
        cycles + " cycles";


    /* --------------------------------
       SAFETY WARNING
    -------------------------------- */

    if (temperature > 45) {

        warningBox.classList.remove("hidden");

        warningText.textContent =
            "The entered temperature is elevated. Do not use the battery based on this prototype result alone. Professional thermal and electrical safety testing is required.";

    }

    else if (resistance > 120) {

        warningBox.classList.remove("hidden");

        warningText.textContent =
            "The entered internal resistance is high. Additional diagnostic testing is required before any reuse decision.";

    }

    else {

        warningBox.classList.add("hidden");

    }


    /* --------------------------------
       SHOW RESULTS
    -------------------------------- */

    resultSection.classList.remove("hidden");

    resultSection.scrollIntoView({
        behavior: "smooth"
    });

});


/* --------------------------------
   APPLICATION DISPLAY
-------------------------------- */

function showApplications(applications) {

    applicationList.innerHTML = "";

    applications.forEach(function (application) {

        const item =
            document.createElement("div");

        item.className =
            "application-item";

        item.textContent =
            "✓ " + application;

        applicationList.appendChild(item);

    });

}


/* --------------------------------
   RESET
-------------------------------- */

resetBtn.addEventListener("click", function () {

    form.reset();

    resultSection.classList.add("hidden");

    sohProgress.style.width = "0%";

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

});
