
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
                            <span class="tag-pill">${item.category || "all"}</span>
                            <span class="status-badge ${item.is_active ? 'active' : 'inactive'}">
                                ${item.is_active ? 'Active' : 'Inactive'}
                            </span>
                        </div>
                        <footer class="menu-card-footer">
                            <button type="button" class="btn btn-text edit-item">Edit</button>
                            <button type="button" class="btn btn-text delete-item">Delete</button>
                            <button type="button" class="btn btn-text toggle-item">Toggle Active</button>
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
                    if (!id) return;
                    
                    // Get current data
                    const titleEl = card.querySelector(".menu-card-title");
                    const priceEl = card.querySelector(".menu-card-price");
                    const tagEl = card.querySelector(".tag-pill");
                    const statusEl = card.querySelector(".status-badge");
                    
                    const currentName = titleEl ? titleEl.innerText.trim() : '';
                    const currentPrice = priceEl ? parseFloat(priceEl.innerText.replace(/[^\d.]/g, '')) : 0;
                    const currentCategory = tagEl ? tagEl.innerText.trim() : 'all';
                    const currentActive = statusEl && statusEl.classList.contains('active');

                    const newName = prompt("Item Name", currentName);
                    const newPriceStr = prompt("Price (₹)", currentPrice);
                    const categories = ['all', 'breakfast', 'lunch', 'dinner'];
                    const newCategory = prompt("Category", currentCategory, categories.join(', '));
                    const newActive = confirm("Active?") ? 1 : 0;

                    if (!newName || isNaN(parseFloat(newPriceStr))) {
                        alert("Name and price required");
                        return;
                    }

                    const newPrice = parseFloat(newPriceStr);
                    if (!categories.includes(newCategory)) {
                        alert("Invalid category");
                        return;
                    }

                    try {
                        const resp = await fetch(`/admin/menu-items/${id}`, {
                            method: "PUT",
                            headers: {"Content-Type": "application/json"},
                            body: JSON.stringify({
                                name: newName,
                                price: newPrice,
                                category: newCategory,
                                is_active: newActive
                            }),
                        });
                        const data = await resp.json();
                        if (!resp.ok || !data.success) {
                            alert(data.error || "Update failed");
                            return;
                        }

                        titleEl.innerText = newName;
                        priceEl.innerText = `₹${newPrice}`;
                        tagEl.innerText = newCategory;
                        statusEl.textContent = newActive ? 'Active' : 'Inactive';
                        statusEl.className = `status-badge ${newActive ? 'active' : 'inactive'}`;
                    } catch (e) {
                        console.error("Update error:", e);
                        alert("Update failed");
                    }
                };
            });

            document.querySelectorAll(".toggle-item").forEach((btn) => {
                btn.onclick = async function () {
                    const card = btn.closest(".menu-card");
                    const id = card.dataset.id;
                    if (!id || !confirm("Toggle active status?")) return;
                    
                    try {
                        const resp = await fetch(`/admin/menu-items/${id}/toggle`, {
                            method: "PATCH"
                        });
                        const data = await resp.json();
                        if (!resp.ok) {
                            alert(data.error || "Toggle failed");
                            return;
                        }
                        
                        const statusEl = card.querySelector(".status-badge");
                        const newStatus = data.item.is_active ? 'Active' : 'Inactive';
                        statusEl.textContent = newStatus;
                        statusEl.className = `status-badge ${data.item.is_active ? 'active' : 'inactive'}`;
                        
                        alert(data.message);
                    } catch (e) {
                        console.error("Toggle error:", e);
                        alert("Toggle failed");
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
    // Settings Meal Mode (/admin/settings)
    // ----------------------------------------
    
    if (window.location.pathname === "/admin/settings") {
        const mealButtons = document.querySelectorAll(".meal-mode");
        const modeLabel = document.querySelector("[data-metric='meal-mode-label']");
        const saveButton = document.querySelector("button:has(+ .metric-caption), .btn-primary");
        
        // Load current mode
        async function loadCurrentMode() {
            try {
                const resp = await fetch("/admin/settings");
                const data = await resp.json();
                if (data.meal_mode) {
                    const activeBtn = document.querySelector(`.meal-mode[onclick*="data.meal_mode"]`) || 
                                    Array.from(mealButtons).find(btn => btn.textContent.trim().toLowerCase() === data.meal_mode.toLowerCase());
                    if (activeBtn) {
                        mealButtons.forEach(b => b.classList.remove("active"));
                        activeBtn.classList.add("active");
                    }
                    if (modeLabel) modeLabel.textContent = data.meal_mode;
                }
            } catch (e) {
                console.error("Load mode error:", e);
            }
        }
        
        // Button handlers
        mealButtons.forEach((btn) => {
            btn.dataset.mode = btn.textContent.trim().toLowerCase();
            btn.addEventListener("click", async function () {
                const newMode = this.dataset.mode;
                mealButtons.forEach((b) => b.classList.remove("active"));
                this.classList.add("active");
                
                try {
                    const resp = await fetch("/admin/settings", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({meal_mode: newMode})
                    });
                    const data = await resp.json();
                    if (resp.ok && data.success) {
                        if (modeLabel) modeLabel.textContent = newMode;
                        // Show save feedback
                        this.style.background = "#d1fae5";
                        setTimeout(() => this.style.background = "", 1000);
                    } else {
                        alert(data.error || "Save failed");
                        // Revert UI
                        await loadCurrentMode();
                    }
                } catch (e) {
                    console.error("Save mode error:", e);
                    alert("Save failed");
                    await loadCurrentMode();
                }
            });
        });
        
        // Initial load
        loadCurrentMode();
    }

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
