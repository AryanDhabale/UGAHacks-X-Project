// Simulated user data
const simulatedUserData = {
    username: "JohnDoe",
    level: 1,
    challengesCompleted: 5
};

const loginSection = document.getElementById("loginSection");
const dashboardSection = document.getElementById("dashboardSection");
const welcomeMessage = document.getElementById("welcomeMessage");
const financialData = document.getElementById("financialData");
const gameSelect = document.getElementById("gameSelect");

const balanceSheetPage = document.getElementById("balanceSheetPage");
const ebitdaPage = document.getElementById("ebitdaPage");
const horizontalAnalysisPage = document.getElementById("horizontalAnalysisPage");
const companyFaceOffPage = document.getElementById("companyFaceOffPage");

const backHomeButtons = {
    balanceSheet: document.getElementById("backHomeBalanceSheet"),
    ebitda: document.getElementById("backHomeEbitda"),
    horizontalAnalysis: document.getElementById("backHomeHorizontalAnalysis"),
    companyFaceOff: document.getElementById("backHomeCompanyFaceOff")
};

// Login Logic
document.getElementById("loginBtn").addEventListener("click", () => {
    const username = document.getElementById("usernameInput").value;
    if (username === simulatedUserData.username) {
        // Successfully logged in
        loginSection.style.display = "none";
        dashboardSection.style.display = "block";
        welcomeMessage.textContent = `Welcome, ${simulatedUserData.username}! Level: ${simulatedUserData.level} | Challenges Completed: ${simulatedUserData.challengesCompleted}`;
        loadFinancialData();
    } else {
        document.getElementById("errorMessage").textContent = "User not found or incorrect username.";
    }
});

// Load Financial Data (simulated)
function loadFinancialData() {
    financialData.innerHTML = "<p>Fetching Financial Data...</p>";

    // Simulate fetching financial data
    setTimeout(() => {
        financialData.innerHTML = "<p><strong>BTC Price (Gemini):</strong> 40000 USD</p>";
        financialData.innerHTML += "<p><strong>Latest AAPL Stock Price:</strong> 150 USD</p>";
    }, 1000);
}

// Game selection logic
gameSelect.addEventListener("change", () => {
    const selectedGame = gameSelect.value;
    switch (selectedGame) {
        case "balanceSheet":
            showPage(balanceSheetPage);
            break;
        case "ebitda":
            showPage(ebitdaPage);
            break;
        case "horizontalAnalysis":
            showPage(horizontalAnalysisPage);
            break;
        case "companyFaceOff":
            showPage(companyFaceOffPage);
            break;
        case "home":
            showPage(dashboardSection);
            break;
    }
});

// Show specific page
function showPage(page) {
    [dashboardSection, balanceSheetPage, ebitdaPage, horizontalAnalysisPage, companyFaceOffPage].forEach(p => p.style.display = "none");
    page.style.display = "block";
}

// Back to home logic
backHomeButtons.balanceSheet.addEventListener("click", () => showPage(dashboardSection));
backHomeButtons.ebitda.addEventListener("click", () => showPage(dashboardSection));
backHomeButtons.horizontalAnalysis.addEventListener("click", () => showPage(dashboardSection));
backHomeButtons.companyFaceOff.addEventListener("click", () => showPage(dashboardSection));

// Navbar Links
document.getElementById("homeLink").addEventListener("click", () => showPage(dashboardSection));
document.getElementById("balanceSheetLink").addEventListener("click", () => {
    gameSelect.value = "balanceSheet";
    showPage(balanceSheetPage);
});
document.getElementById("ebitdaLink").addEventListener("click", () => {
    gameSelect.value = "ebitda";
    showPage(ebitdaPage);
});
document.getElementById("horizontalAnalysisLink").addEventListener("click", () => {
    gameSelect.value = "horizontalAnalysis";
    showPage(horizontalAnalysisPage);
});
document.getElementById("companyFaceOffLink").addEventListener("click", () => {
    gameSelect.value = "companyFaceOff";
    showPage(companyFaceOffPage);
});
