
// ============================================
// ADMIN PANEL FRONTEND SCRIPT
// ============================================

document.addEventListener("DOMContentLoaded", function () {
    console.log("Admin panel script initialised");

    // ----------------------------------------
    // Admin Login Handling
    // ----------------------------------------

    const loginForm = document.getElementById("adminLoginForm");
    const loginError = document.getElementById("adminLoginError");
    const loginButton = document.getElementById("adminLoginButton");

    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const emailInput = document.getElementById("adminEmail");
            const passwordInput = document.getElementById("adminPassword");

            if (!emailInput || !passwordInput) {
                return;
            }

            const email = emailInput.value.trim();
            const password = passwordInput.value;

            if (!email || !password) {
                showLoginError("Please enter both email and password.");
                return;
            }

            try {
                if (loginButton) {
                    loginButton.disabled = true;
                    loginButton.textContent = "Signing in...";
                }

                const response = await fetch("/admin/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json().catch(() => ({}));

                if (response.ok && data && data.success) {
                    window.location.href = "/admin/dashboard";
                    return;
                }

                const message =
                    (data && (data.error || data.message)) ||
                    "Login failed. Please check your credentials.";
                showLoginError(message);
            } catch (error) {
                console.error("Admin login error:", error);
                showLoginError("Unable to connect. Please try again.");
            } finally {
                if (loginButton) {
                    loginButton.disabled = false;
                    loginButton.textContent = "Sign in";
                }
            }
        });
    }

    function showLoginError(message) {
        if (!loginError) return;
        loginError.textContent = message;
        loginError.hidden = false;
    }

    // ----------------------------------------
    // Sidebar Toggle (Responsive)
    // ----------------------------------------

    const sidebar = document.querySelector(".admin-sidebar");
    const sidebarToggle = document.querySelector(".sidebar-toggle");

    if (sidebar && sidebarToggle) {
        sidebarToggle.addEventListener("click", () => {
            sidebar.classList.toggle("is-open");
        });

        document.addEventListener("click", (event) => {
            if (
                window.innerWidth <= 960 &&
                sidebar.classList.contains("is-open") &&
                !sidebar.contains(event.target) &&
                event.target !== sidebarToggle
            ) {
                sidebar.classList.remove("is-open");
            }
        });
    }

    // ----------------------------------------
    // Sidebar Active Navigation
    // ----------------------------------------

    const navLinks = document.querySelectorAll(".sidebar-link");
    const path = window.location.pathname;

    navLinks.forEach((link) => {
        const href = link.getAttribute("href") || "";
        if (href && path.startsWith(href)) {
            link.classList.add("active");
        }

        link.addEventListener("click", () => {
            navLinks.forEach((l) => l.classList.remove("active"));
            link.classList.add("active");
        });
    });

    // ----------------------------------------
    // Generic Search Filters
    // ----------------------------------------

    const userSearch = document.querySelector("#userSearch");
    if (userSearch) {
        userSearch.addEventListener("input", function () {
            const value = this.value.toLowerCase();
            const rows = document.querySelectorAll("#usersTable tr");
            rows.forEach((row) => {
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(value) ? "" : "none";
            });
        });
    }

    const orderSearch = document.querySelector("#orderSearch");
    if (orderSearch) {
        orderSearch.addEventListener("input", function () {
            const value = this.value.toLowerCase();
            const table = document.querySelector("#ordersTable") || document.querySelector("#recentOrdersBody");
            if (!table) return;

            const rows = table.querySelectorAll("tr");
            rows.forEach((row) => {
                if (row.classList.contains("placeholder-row")) return;
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(value) ? "" : "none";
            });
        });
    }

    // ----------------------------------------
    // Menu Item Interactions (other admin pages)
    // ----------------------------------------

    document.querySelectorAll(".delete-item").forEach((btn) => {
        btn.addEventListener("click", function () {
            const card = btn.closest(".menu-card");
            if (!card) return;
            if (confirm("Delete this menu item?")) {
                card.remove();
            }
        });
    });

    document.querySelectorAll(".edit-item").forEach((btn) => {
        btn.addEventListener("click", function () {
            const card = btn.closest(".menu-card");
            if (!card) return;
            const title = card.querySelector("h3");
            if (!title) return;
            const newName = prompt("Edit item name", title.innerText);
            if (newName) {
                title.innerText = newName;
            }
        });
    });

    // ----------------------------------------
    // Order Status Change (other admin pages)
    // ----------------------------------------

    document.querySelectorAll(".status-select").forEach((select) => {
        select.addEventListener("change", function () {
            const status = select.value;
            const badge = select.parentElement.querySelector(".status-badge");
            if (!badge) return;
            badge.innerText = status;
            badge.className = "status-badge " + status.toLowerCase();
        });
    });

    // ----------------------------------------
    // Settings Meal Mode (other admin pages)
    // ----------------------------------------

    const mealButtons = document.querySelectorAll(".meal-mode");
    mealButtons.forEach((btn) => {
        btn.addEventListener("click", function () {
            mealButtons.forEach((b) => b.classList.remove("active"));
            btn.classList.add("active");
        });
    });

    // ----------------------------------------
    // Dashboard Metric Placeholders
    // ----------------------------------------

    document.querySelectorAll("[data-metric]").forEach((el) => {
        if (!el.textContent || !el.textContent.trim()) {
            el.textContent = "--";
        }
    });

    // ----------------------------------------
    // Dashboard Charts (empty data placeholders)
    // ----------------------------------------

    if (typeof Chart !== "undefined") {
        const revenueCanvas = document.getElementById("revenueChart");
        if (revenueCanvas) {
            new Chart(revenueCanvas, {
                type: "line",
                data: {
                    labels: [],
                    datasets: [
                        {
                            label: "Revenue",
                            data: [],
                            borderColor: "#22c55e",
                            borderWidth: 2,
                            tension: 0.45,
                            fill: false
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { display: false } },
                        y: { grid: { color: "rgba(55, 65, 81, 0.55)" } }
                    }
                }
            });
        }

        const categoryCanvas = document.getElementById("categoryChart");
        if (categoryCanvas) {
            new Chart(categoryCanvas, {
                type: "bar",
                data: {
                    labels: [],
                    datasets: [
                        {
                            label: "Categories",
                            data: [],
                            backgroundColor: "#22c55e",
                            borderRadius: 6
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { display: false } },
                        y: { grid: { color: "rgba(55, 65, 81, 0.55)" } }
                    }
                }
            });
        }

        const orderCanvas = document.getElementById("orderChart");
        if (orderCanvas) {
            new Chart(orderCanvas, {
                type: "doughnut",
                data: {
                    labels: [],
                    datasets: [
                        {
                            data: [],
                            backgroundColor: ["#f59e0b", "#3b82f6", "#22c55e"],
                            borderWidth: 0
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    cutout: "72%"
                }
            });
        }
    }
});
