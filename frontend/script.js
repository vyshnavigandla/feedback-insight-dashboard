document.addEventListener("DOMContentLoaded", () => {
    const dataForm = document.getElementById("dataForm");

    // ---------------- 1. SUBMITTING THE FORM (index.html) ----------------
    if (dataForm) {
        dataForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(dataForm);
            const payload = Object.fromEntries(formData.entries());

            // Added validations to ensure data integrity
            if (!payload.product_name || !payload.rating) {
                showResponse("Please fill in the required fields.", "red");
                return;
            }

            try {
                const response = await fetch("http://localhost:5000/api/feedback/submit", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    showResponse("✔ Feedback submitted successfully!", "green");
                    dataForm.reset();
                } else {
                    const result = await response.json();
                    const errorMsg = result.errors ? result.errors.join(", ") : result.message;
                    showResponse(`⚠ ${errorMsg}`, "red");
                }
            } catch (err) {
                showResponse("Backend is not running. Please run 'python app.py'", "red");
            }
        });
    }

    // ---------------- 2. DASHBOARD LOGIC (dashboard.html) ----------------
    if (document.querySelector(".dashboard") || document.getElementById("tableBody")) {
        loadDashboardData();
        
        // Manual Refresh
        document.getElementById("refreshBtn")?.addEventListener("click", loadDashboardData);

        // Auto-refresh logic (10s) as per your checkbox
        setInterval(() => {
            if (document.getElementById("autoRefresh")?.checked) {
                loadDashboardData();
            }
        }, 10000);
    }
});

// UI Helper for form messages
function showResponse(text, color) {
    const msgDiv = document.getElementById("responseMessage");
    if (msgDiv) {
        msgDiv.style.display = "block";
        msgDiv.style.color = color;
        msgDiv.innerText = text;
    }
}

// ---------------- 3. FETCHING DATA & AI SYNC ----------------
async function loadDashboardData() {
    try {
        // Fetch raw records and AI analysis
        const [recordsRes, statsRes] = await Promise.all([
            fetch("http://localhost:5000/api/feedback/all"),
            fetch("http://localhost:5000/api/analysis/stats")
        ]);

        const records = await recordsRes.json();
        const stats = await statsRes.json();

        // --- UPDATE SUMMARY CARDS ---
        // Total Records
        document.getElementById("totalSubmissions").textContent = records.length;
        
        // Average Rating Calculation
        const avg = records.length > 0 
            ? (records.reduce((acc, r) => acc + parseFloat(r.rating), 0) / records.length).toFixed(1) 
            : "0.0";
        document.getElementById("avgRating").textContent = avg;

        // HIGH PRIORITY SYNC (Fixes the "0" issue)
        // Explicitly counts records with 1 or 2 star ratings
        const urgentCount = records.filter(r => parseInt(r.rating) <= 2).length;
        document.getElementById("urgentCount").textContent = urgentCount;

        // SATISFACTION SYNC
        const sentiment = stats.sentiment_summary || (avg >= 4 ? "Positive" : avg <= 2 ? "Negative" : "Neutral");
        document.getElementById("sentimentScore").textContent = sentiment;

        // --- UPDATE AI PROCESSED INSIGHTS ---
        // These target the specific text IDs in your insights row
        document.getElementById("aiSentiment").textContent = `Overall mood is ${sentiment.toLowerCase()}.`;
        document.getElementById("aiSuggestion").textContent = stats.ai_suggestion || "Monitor low-rated product categories.";

        // --- UPDATE UI COMPONENTS ---
        updateTable(records);
        renderCharts(records);
        
        document.getElementById("lastUpdated").textContent = new Date().toLocaleTimeString();
        document.getElementById("dashboardStatus").innerHTML = "● Online";

    } catch (error) {
        console.error("Dashboard Sync Error:", error);
        const status = document.getElementById("dashboardStatus");
        if (status) status.innerHTML = "● Offline";
    }
}

// ---------------- 4. TABLE RENDERING (7 Columns) ----------------
function updateTable(records) {
    const tableBody = document.getElementById("tableBody");
    if (!tableBody) return;

    if (records.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="7">No records found.</td></tr>`;
        return;
    }

    tableBody.innerHTML = records.map(r => {
        const isUrgent = parseInt(r.rating) <= 2;
        const priorityTag = isUrgent 
            ? '<b style="color: #ff4d4d;">URGENT</b>' 
            : '<span style="color: #2ecc71;">Normal</span>';

        return `
        <tr>
            <td><strong>${r.name || "Anonymous"}</strong></td>
            <td>${r.product_name}</td>
            <td>${r.feedback_type}</td>
            <td>${priorityTag}</td>
            <td>${r.rating} ⭐</td>
            <td>${r.satisfaction}</td>
            <td title="${r.comments}">${r.comments ? r.comments.substring(0, 25) + "..." : "N/A"}</td>
        </tr>`;
    }).join("");
}

// ---------------- 5. CHART RENDERING (Plotly) ----------------
function renderCharts(records) {
    if (!records || records.length === 0) return;

    // --- Pie Chart (Categories) ---
    const counts = {};
    records.forEach(r => counts[r.feedback_type] = (counts[r.feedback_type] || 0) + 1);

    Plotly.newPlot("categoryChart", [{
        labels: Object.keys(counts),
        values: Object.values(counts),
        type: 'pie',
        marker: { colors: ['#4e73df', '#1cc88a', '#36b9cc'] }
    }], { height: 250, margin: { t: 10, b: 10, l: 10, r: 10 } });

    // --- Rating Trend Chart ---
    Plotly.newPlot("trendChart", [{
        x: records.map(r => r.timestamp),
        y: records.map(r => r.rating),
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#4e73df', shape: 'spline' }
    }], { 
        height: 250, 
        margin: { t: 10, b: 40, l: 40, r: 10 },
        yaxis: { range: [0, 5.5] } 
    });
}