
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

    // Menu item management on /admin/menu (backed by database)
    if (window.location.pathname.startsWith("/admin/menu")) {
        const menuGrid = document.getElementById("menuGrid");
        const addButton = document.querySelector(".menu-add-button");

        async function fetchMenuItems() {
            if (!menuGrid) return;
            menuGrid.innerHTML = '<p style="padding:1rem;color:#6b7280;">Loading menu items…</p>';
            try {
                const response = await fetch("/menu-items");
                if (!response.ok) {
                    throw new Error("Failed to load menu items");
                }
                const items = await response.json();
                if (!items || items.length === 0) {
                    menuGrid.innerHTML = '<p style="padding:1rem;color:#6b7280;">No menu items found. Use “Add Item” to create one.</p>';
                    return;
                }

                menuGrid.innerHTML = "";
                items.forEach((item) => {
                    const card = document.createElement("article");
                    card.className = "menu-card";
                    card.dataset.id = item.id;
                    card.innerHTML = `
                        <header class="menu-card-header">
                            <h2 class="menu-card-title">${item.name}</h2>
                            <span class="menu-card-price">₹${item.price}</span>
                        </header>
                        <p class="menu-card-description">
                            ${item.description || "No description"}
                        </p>
                        <div class="menu-card-tags">
                            <span class="tag-pill">${item.category || "uncategorized"}</span>
                        </div>
                        <footer class="menu-card-footer">
                            <button type="button" class="btn btn-text edit-item">Edit</button>
                            <button type="button" class="btn btn-text delete-item">Delete</button>
                        </footer>
                    `;
                    menuGrid.appendChild(card);
                });

                attachMenuCardHandlers();
            } catch (error) {
                console.error("Error loading admin menu items:", error);
                menuGrid.innerHTML = '<p style="padding:1rem;color:#b91c1c;">Failed to load menu items from the database.</p>';
            }
        }

        function attachMenuCardHandlers() {
            document.querySelectorAll(".delete-item").forEach((btn) => {
                btn.onclick = async function () {
                    const card = btn.closest(".menu-card");
                    if (!card) return;
                    const id = card.dataset.id;
                    if (!id) return;
                    if (!confirm("Delete this menu item?")) return;
                    try {
                        const resp = await fetch(`/admin/menu-items/${id}`, {
                            method: "DELETE",
                        });
                        if (!resp.ok) {
                            const data = await resp.json().catch(() => ({}));
                            alert(data.error || "Failed to delete item");
                            return;
                        }
                        card.remove();
                        if (!menuGrid.children.length) {
                            menuGrid.innerHTML = '<p style="padding:1rem;color:#6b7280;">No menu items found. Use “Add Item” to create one.</p>';
                        }
                    } catch (e) {
                        console.error("Delete menu item error:", e);
                        alert("Unable to delete item. Please try again.");
                    }
                };
            });

            document.querySelectorAll(".edit-item").forEach((btn) => {
                btn.onclick = async function () {
                    const card = btn.closest(".menu-card");
                    if (!card) return;
                    const id = card.dataset.id;
                    const titleEl = card.querySelector(".menu-card-title");
                    const priceEl = card.querySelector(".menu-card-price");
                    if (!titleEl || !priceEl) return;

                    const currentName = titleEl.innerText.trim();
                    const currentPrice = parseFloat(
                        (priceEl.innerText.replace(/[^\d.]/g, "") || "0")
                    );

                    const newName = prompt("Edit item name", currentName) ?? currentName;
                    const newPriceStr = prompt(
                        "Edit item price (₹)",
                        isNaN(currentPrice) ? "" : currentPrice.toString()
                    );
                    const newPrice =
                        newPriceStr !== null && newPriceStr.trim() !== ""
                            ? parseFloat(newPriceStr)
                            : currentPrice;

                    if (!newName || isNaN(newPrice)) {
                        alert("Name and price are required.");
                        return;
                    }

                    try {
                        const resp = await fetch(`/admin/menu-items/${id}`, {
                            method: "PUT",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({
                                name: newName,
                                price: newPrice,
                            }),
                        });
                        const data = await resp.json().catch(() => ({}));
                        if (!resp.ok || !data.success) {
                            alert(data.error || "Failed to update item");
                            return;
                        }

                        const item = data.item || {};
                        titleEl.innerText = item.name || newName;
                        priceEl.innerText = `₹${item.price ?? newPrice}`;
                    } catch (e) {
                        console.error("Update menu item error:", e);
                        alert("Unable to update item. Please try again.");
                    }
                };
            });
        }

        if (addButton) {
            addButton.addEventListener("click", async () => {
                const name = prompt("Enter item name");
                if (!name) return;
                const priceStr = prompt("Enter price (₹)");
                if (!priceStr || !priceStr.trim()) return;
                const price = parseFloat(priceStr);
                if (isNaN(price)) {
                    alert("Invalid price.");
                    return;
                }

                try {
                    const resp = await fetch("/admin/menu-items", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            name,
                            price,
                        }),
                    });
                    const data = await resp.json().catch(() => ({}));
                    if (!resp.ok || !data.success) {
                        alert(data.error || "Failed to create item");
                        return;
                    }
                    // Reload list to include new item
                    await fetchMenuItems();
                } catch (e) {
                    console.error("Create menu item error:", e);
                    alert("Unable to create item. Please try again.");
                }
            });
        }

        // Initial load
        fetchMenuItems();
    }

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
