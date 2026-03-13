 // Login function for email/password login
async function loginUser(e) {
  e.preventDefault();
  const email = document.getElementById('loginEmail').value;
  const password = document.getElementById('loginPassword').value;

  try {
    const response = await fetch('http://127.0.0.1:3000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Login failed');
    }

    // Store email for OTP verification
    localStorage.setItem('loginEmail', email);

    // Hide login button and form, show OTP section
    document.getElementById('loginBtn').style.display = 'none';
    document.querySelector('form').style.display = 'none';
    document.getElementById('otpSection').style.display = 'block';

    // Send OTP to user's email
    await sendOtp(email);

  } catch (error) {
    alert('Error logging in: ' + error.message);
  }

  return false;
}

// Function to send OTP to email
async function sendOtp(email) {
  try {
    const response = await fetch('http://127.0.0.1:3000/send-login-otp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email: email })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to send OTP');
    }

    // Store OTP ID and expiry time (5 minutes from now)
    localStorage.setItem('otpId', data.otpId);
    localStorage.setItem('otpExpiry', Date.now() + 300000); // 5 minutes in milliseconds

    // Show success message
    document.getElementById('otpMessage').textContent = 'OTP sent to your email!';
    
    // Start timer
    startTimer();

  } catch (error) {
    alert('Error sending OTP: ' + error.message);
    // Show login form again if OTP fails
    document.getElementById('loginBtn').style.display = 'block';
    document.querySelector('form').style.display = 'block';
    document.getElementById('otpSection').style.display = 'none';
  }
}

// Existing function: registerUser
async function registerUser(e) {
  if (e) {
    e.preventDefault();
    e.stopPropagation();
  }
  
  const name = document.getElementById('regName').value;
  const email = document.getElementById('regEmail').value;
  const password = document.getElementById('regPassword').value;
  const mobile = document.getElementById('regMobile').value;

  try {
    const response = await fetch('http://127.0.0.1:3000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name, email, password, mobile })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Registration failed');
    }

    alert('Registration successful! Please login.');

    // Switch to Login form (slide back)
    showLoginPanel();

    // Optionally clear the register form
    document.getElementById('regName').value = '';
    document.getElementById('regMobile').value = '';
    document.getElementById('regEmail').value = '';
    document.getElementById('regPassword').value = '';

  } catch (error) {
    alert('Error registering user: ' + error.message);
  }

  return false;
}




// Existing function: logout
function logout() {
  alert('Logged out successfully!');
  localStorage.clear(); // Clear all localStorage data
  window.location.href = '/login'; // Redirect to login page
}

// --- NEW PROFILE FUNCTIONS ---

// Function to load profile data when the profile page opens
async function loadProfile() {
    const localUser = JSON.parse(localStorage.getItem('user')) || {};
    if (!localUser.mobile) {
        alert('User data not found. Please login again.');
        window.location.href = '/login';
        return;
    }

    try {
        // Fetch latest user data from server
        const response = await fetch('http://127.0.0.1:3000/check-user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mobile: localUser.mobile })
        });

        if (!response.ok) {
            throw new Error('Failed to fetch user data');
        }

        const data = await response.json();
        if (!data.exists) {
            alert('User not found. Please login again.');
            localStorage.clear();
            window.location.href = '/login';
            return;
        }

        const user = data.user;
        // Update localStorage with latest data
        localStorage.setItem('user', JSON.stringify(user));

        // Populate header display elements
        if (document.getElementById('profileDisplayName')) {
            document.getElementById('profileDisplayName').textContent = user.name || 'User';
        }
        if (document.getElementById('profileDisplayEmail')) {
            document.getElementById('profileDisplayEmail').textContent = user.email || '';
        }
        // Update avatar with first letter of name
        const avatar = document.querySelector('.avatar');
        if (avatar) {
            avatar.textContent = (user.name || 'U').charAt(0).toUpperCase();
        }

        // Populate table display elements
        if (document.getElementById('profileNameDisplay')) {
            document.getElementById('profileNameDisplay').textContent = user.name || '-';
            document.getElementById('profileEmailDisplay').textContent = user.email || '-';
            document.getElementById('profileMobileDisplay').textContent = user.mobile || '-';
            document.getElementById('profileDOBDisplay').textContent = user.dob ? new Date(user.dob).toLocaleDateString() : '-';
            document.getElementById('profileGenderDisplay').textContent = user.gender || '-';
        }

        // Populate form elements for editing
        if (document.getElementById('profileForm')) {
            document.getElementById('profileName').value = user.name || '';
            document.getElementById('profileMobile').value = user.mobile || '';
            document.getElementById('profileEmail').value = user.email || '';
            document.getElementById('profileDOB').value = user.dob || '';
            document.getElementById('profileGender').value = user.gender || '';
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        alert('Error loading profile data. Please try again.');
        // Fallback to localStorage data
        const user = localUser;

        // Populate header display elements
        if (document.getElementById('profileDisplayName')) {
            document.getElementById('profileDisplayName').textContent = user.name || 'User';
        }
        if (document.getElementById('profileDisplayEmail')) {
            document.getElementById('profileDisplayEmail').textContent = user.email || '';
        }
        // Update avatar with first letter of name
        const avatar = document.querySelector('.avatar');
        if (avatar) {
            avatar.textContent = (user.name || 'U').charAt(0).toUpperCase();
        }

        // Populate table display elements
        if (document.getElementById('profileNameDisplay')) {
            document.getElementById('profileNameDisplay').textContent = user.name || '-';
            document.getElementById('profileEmailDisplay').textContent = user.email || '-';
            document.getElementById('profileMobileDisplay').textContent = user.mobile || '-';
            document.getElementById('profileDOBDisplay').textContent = user.dob ? new Date(user.dob).toLocaleDateString() : '-';
            document.getElementById('profileGenderDisplay').textContent = user.gender || '-';
        }

        // Populate form elements for editing
        if (document.getElementById('profileForm')) {
            document.getElementById('profileName').value = user.name || '';
            document.getElementById('profileMobile').value = user.mobile || '';
            document.getElementById('profileEmail').value = user.email || '';
            document.getElementById('profileDOB').value = user.dob || '';
            document.getElementById('profileGender').value = user.gender || '';
        }
    }
}

// Function to handle profile update
async function updateProfile(e) {
    e.preventDefault();

    const user = JSON.parse(localStorage.getItem('user')) || {};
    const mobile = user.mobile;

    const updatedProfileData = {
        mobile: mobile,
        name: document.getElementById('name').value,
        dob: document.getElementById('dob').value,
        gender: document.getElementById('gender').value
    };

    try {
    const response = await fetch('http://127.0.0.1:3000/update-profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedProfileData)
        });

        if (!response.ok) {
            throw new Error('Profile update failed');
        }

        const data = await response.json();
        // Update localStorage with the updated user from server
        localStorage.setItem('user', JSON.stringify(data.user));

        alert('Profile Updated Successfully!');
    } catch (error) {
        alert('Error updating profile: ' + error.message);
    }

    return false;
}



// Get the main container for animation
const mainContainer = document.querySelector('.login-main');

// Function to show the Register form (Slides to the left)
function showRegisterPanel(e) {
    if (e) e.preventDefault();
    if (mainContainer) {
        mainContainer.classList.add('register-active');
        document.title = 'Cafe Zone | Register'; // Change page title dynamically
    }
}

// Function to show the Login form (Slides back to the right)
function showLoginPanel(e) {
    if (e) e.preventDefault();
    
    // Check if we're on login page with animation container, otherwise redirect
    const mainContainer = document.querySelector('.login-main');
    if (!mainContainer || !document.querySelector('.animation-container')) {
        // We're on standalone register.html - redirect to login page instead of animating
        window.location.href = '/login';
        return;
    }
    
    mainContainer.classList.remove('register-active');
    document.title = 'Cafe Zone | Login'; // Change page title dynamically
}


// Function to toggle the navigation menu
function toggleNavMenu() {
    const navMenu = document.getElementById('navMenu');
    if (navMenu) {
        navMenu.classList.toggle('active');
    }
}

// Global variable to store timer interval ID
let otpTimerInterval;

// Function to generate OTP (API call) - SECURE: Calls backend to send OTP
async function generateOtp() {
  const email = document.getElementById('loginEmail').value;

  if (!email) {
    alert('Please enter your email address');
    return;
  }

  try {
    // Call the secure backend endpoint to send OTP
    const response = await fetch('http://127.0.0.1:3000/send-login-otp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email: email })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to send OTP');
    }

    // Store the OTP ID returned by backend (not the OTP itself!)
    localStorage.setItem('otpId', data.otpId);
    // Store expiry time (5 minutes from now)
    localStorage.setItem('otpExpiry', Date.now() + 300000); // 5 minutes in milliseconds

    // Show OTP section
    document.getElementById('otpSection').style.display = 'block';
    document.getElementById('sendOtpBtn').style.display = 'none';
    document.getElementById('otpMessage').textContent = 'Sending OTP to your email...';

    // Start timer (5 minutes as configured in backend)
    startTimer();

    document.getElementById('otpMessage').textContent = `OTP sent to your email successfully!`;
  } catch (error) {
    alert('Error sending login OTP: ' + error.message);
  }
}

// Function to start OTP timer
function startTimer() {
  // Clear any existing timer
  if (otpTimerInterval) {
    clearInterval(otpTimerInterval);
  }

  let timeLeft = 300; // 5 minutes (matches backend expiry)
  const timerDisplay = document.getElementById('timerDisplay');
  const resendBtn = document.getElementById('resendOtpBtn');

  otpTimerInterval = setInterval(() => {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    timerDisplay.textContent = `Time remaining: ${minutes}:${seconds.toString().padStart(2, '0')}`;
    timeLeft--;

    if (timeLeft < 0) {
      clearInterval(otpTimerInterval);
      timerDisplay.textContent = 'OTP expired!';
      resendBtn.style.display = 'block';
    }
  }, 1000);
}

// Function to resend OTP
function resendOtp() {
  generateOtp();
  document.getElementById('resendOtpBtn').style.display = 'none';
}

// Function to show intermediate popup
function showIntermediatePopup() {
  const intermediatePopup = document.getElementById('intermediatePopup');
  const intermediateOkBtn = document.getElementById('intermediateOkBtn');
  const intermediateCancelBtn = document.getElementById('intermediateCancelBtn');

  if (intermediatePopup && intermediateOkBtn && intermediateCancelBtn) {
    intermediatePopup.style.display = 'flex';

    // Add event listeners
    intermediateOkBtn.addEventListener('click', () => {
      intermediatePopup.style.display = 'none';
      showDietPopup();
    });
    intermediateCancelBtn.addEventListener('click', () => {
      intermediatePopup.style.display = 'none';
      localStorage.removeItem('dietPreference');
      loadFoodItems();
    });
  }
}

// Function to show diet popup with smooth animation
function showDietPopup() {
  const dietPopup = document.getElementById('dietPopup');
  const dietBtn = document.getElementById('dietBtn');
  const nonDietBtn = document.getElementById('nonDietBtn');
  const cancelBtn = document.getElementById('cancelBtn');

  if (dietPopup && dietBtn && nonDietBtn && cancelBtn) {
    // Reset animation by removing and re-adding the class
    dietPopup.style.display = 'flex';
    dietPopup.classList.remove('popup-overlay');
    void dietPopup.offsetWidth; // Trigger reflow
    dietPopup.classList.add('popup-overlay');

    // Add event listeners for diet buttons with animation
    dietBtn.addEventListener('click', () => handleDietSelection('diet'));
    nonDietBtn.addEventListener('click', () => handleDietSelection('non-diet'));
    cancelBtn.addEventListener('click', () => handleDietSelection('cancel'));
  }
}

// Function to hide popup with fade out animation
function hidePopup(popupId) {
  const popup = document.getElementById(popupId);
  if (popup) {
    popup.style.animation = 'fadeOut 0.3s ease forwards';
    setTimeout(() => {
      popup.style.display = 'none';
      popup.style.animation = '';
    }, 300);
  }
}

// Function to handle diet selection
function handleDietSelection(dietPreference) {
  localStorage.setItem('dietPreference', dietPreference);
  document.getElementById('dietPopup').style.display = 'none';
  loadFoodItems();
}

// Function to save logged-in user's basic info in localStorage 
function saveUserToLocal(userInfo) { 
	localStorage.setItem("user", JSON.stringify({ 
		id: userInfo.id,
		name: userInfo.name,
		email:	userInfo.email 
	}));
}

// Function to verify OTP (API call)
async function verifyOtp() {
  console.log('verifyOtp called');
  // Only allow OTP verification on login page (served at / or /login)
  if (window.location.pathname !== '/' && !window.location.pathname.includes('login.html')) {
    console.log('Not on login page');
    return;
  }

  const enteredOtp = document.getElementById('otpInput').value.trim();
  console.log('Entered OTP:', enteredOtp);
  const otpId = localStorage.getItem('otpId');
  console.log('OTP ID:', otpId);

  try {
    const response = await fetch('http://127.0.0.1:3000/verify-login-otp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ otpId: otpId, otp: enteredOtp })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Verification failed');
    }

    if (data.success) {
      // Fetch user data after successful login
      const email = document.getElementById('loginEmail').value;
      const checkResponse = await fetch('http://127.0.0.1:3000/check-user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email })
      });

      if (checkResponse.ok) {
        const checkData = await checkResponse.json();
        if (checkData.exists) {
          localStorage.setItem('user', JSON.stringify(checkData.user));
        }
      }

      // Always redirect to cafeteria after successful login
      window.location.href = '/cafeteria';
    } else {
      // Invalid OTP - redirect to register page for MFA setup
      alert('Invalid OTP! Redirecting to registration for security verification.');
      window.location.href = '/register';
    }
  } catch (error) {
    alert('Error verifying OTP: ' + error.message);
  }
}





// Global cart storage
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Function to save cart to localStorage
function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

// Function to update cart count display (if you have a cart icon)
function updateCartCount() {
    const cartCount = document.getElementById('cart-count');
    if (cartCount) {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCount.textContent = totalItems;
    }
}

// Function to show add to cart confirmation popup
function showAddToCartConfirmation(itemId, name, price, image_url, protein, carbs, fats, calories) {
    const popup = document.getElementById('addToCartPopup');
    const confirmBtn = document.getElementById('confirmAddBtn');
    const cancelBtn = document.getElementById('cancelAddBtn');

    if (popup && confirmBtn && cancelBtn) {
        popup.style.display = 'flex';

        // Remove previous event listeners
        const newConfirmBtn = confirmBtn.cloneNode(true);
        const newCancelBtn = cancelBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
        cancelBtn.parentNode.replaceChild(newCancelBtn, cancelBtn);

        // Add event listeners
        newConfirmBtn.addEventListener('click', () => {
            popup.style.display = 'none';
            addToCart(itemId, name, price, image_url, protein, carbs, fats, calories);
        });
        newCancelBtn.addEventListener('click', () => {
            popup.style.display = 'none';
        });
    }
}

// Function to add item to cart
function addToCart(itemId, name, price, image_url, protein, carbs, fats, calories) {
    const itemName = name || 'Item';
    const existingItem = cart.find(item => item.id === itemId);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: itemId,
            name: itemName,
            price: parseFloat(price),
            image_url: image_url,
            protein: parseFloat(protein || 0),
            carbs: parseFloat(carbs || 0),
            fats: parseFloat(fats || 0),
            calories: parseFloat(calories || 0),
            quantity: 1
        });
    }
    saveCart();
    updateCartCount();
    // Show success popup instead of alert
    showAddedToCartPopup(itemName);
}

// Function to show added to cart success popup
function showAddedToCartPopup(itemName) {
    // Create a temporary popup for success message
    const successPopup = document.createElement('div');
    successPopup.style.position = 'fixed';
    successPopup.style.inset = '0';
    successPopup.style.background = 'rgba(0,0,0,0.5)';
    successPopup.style.zIndex = '10000';
    successPopup.style.display = 'flex';
    successPopup.style.alignItems = 'center';
    successPopup.style.justifyContent = 'center';

    successPopup.innerHTML = `
        <div style="background:#fff;border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,0.2);width:400px;max-width:90%;padding:26px;text-align:center;">
            <div style="width:64px;height:64px;margin:0 auto 12px auto;border-radius:50%;background:#4CAF50;display:flex;align-items:center;justify-content:center;font-size:26px;color:#fff;">✓</div>
            <div style="font-weight:800;color:#333;font-size:20px;margin-bottom:6px;">Added to Cart!</div>
            <div style="color:#666;margin-bottom:14px;">${itemName} has been added to your cart.</div>
            <button style="background:#4CAF50;color:#fff;border:none;padding:10px 20px;border-radius:6px;cursor:pointer;" onclick="this.parentElement.parentElement.remove()">OK</button>
        </div>
    `;

    document.body.appendChild(successPopup);

    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (document.body.contains(successPopup)) {
            document.body.removeChild(successPopup);
        }
    }, 3000);
}

// Function to increase quantity
function increaseQuantity(itemId) {
    const quantityElement = document.getElementById(`quantity-${itemId}`);
    let quantity = parseInt(quantityElement.textContent);
    quantityElement.textContent = quantity + 1;
}

// Function to decrease quantity
function decreaseQuantity(itemId) {
    const quantityElement = document.getElementById(`quantity-${itemId}`);
    let quantity = parseInt(quantityElement.textContent);
    if (quantity > 1) {
        quantityElement.textContent = quantity - 1;
    }
}

// Function to create nutrition chart
function createNutritionChart(canvasId, protein, carbs, fats, calories) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Protein', 'Carbs', 'Fats'],
            datasets: [{
                data: [protein, carbs, fats],
                backgroundColor: [
                    '#FF6384', // Protein - Red
                    '#36A2EB', // Carbs - Blue
                    '#FFCE56'  // Fats - Yellow
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        font: {
                            size: 10
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${value}g (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Function to load food items from database menu-items API (primary) with fallback
async function loadFoodItems(){
    try {
        // Try to fetch from menu-items API first (database)
        const response = await fetch("http://127.0.0.1:3000/menu-items")
        if (response.ok) {
            const items = await response.json()
            const menuGrid = document.querySelector(".menu-grid")
            if (!menuGrid) return;
            menuGrid.innerHTML = ""
            items.forEach(item => {
                menuGrid.innerHTML += `
                <div class="menu-item menu-card">
                    <div class="image-block">
                        <img src="${item.image_url}" class="item-image">
                    </div>
                    <div class="item-details">
                        <h3 class="item-title">${item.name}</h3>
                        <p class="item-price">₹${item.price}</p>
                        <button class="add-to-cart-btn" onclick="addToCart(${item.id},'${item.name}',${item.price})">Add to Cart</button>
                    </div>
                </div>
                `
            })
            return;
        }
    } catch (_) { /* ignore and fall through to fallback */ }
    
    // Fallback: Try food-items API
    try {
        let foodItems = [];
        const response = await fetch('http://127.0.0.1:3000/food-items');
        if (response.ok) {
            foodItems = await response.json();
            try { localStorage.setItem('cachedFoodItems', JSON.stringify(foodItems)); } catch (_) {}
        }
        
        // CSV fallback
        if (!foodItems || foodItems.length === 0) {
            const csvItems = await loadItemsFromCsvPaths(['FoodItem_export_clean.csv', 'fooditem_export.csv','item_export.csv']);
            if (csvItems && csvItems.length) foodItems = csvItems;
        }

        // Try cached
        if (!foodItems || foodItems.length === 0) {
            const cached = JSON.parse(localStorage.getItem('cachedFoodItems') || '[]');
            if (cached.length) foodItems = cached;
        }

        // Built-in sample to ensure page never looks empty
        if (!foodItems || foodItems.length === 0) {
            foodItems = [
                { id:'sample1', name:'Sprouts Chaat', price:110, image_url:'images/pizza1.jpeg', protein:18, carbs:28, fats:6, calories:230, category:'diet', description:'Light and protein rich.' },
                { id:'sample2', name:'Paneer Tikka', price:280, image_url:'images/indian.jpeg', protein:24, carbs:45, fats:28, calories:550, category:'diet', description:'Creamy classic.' },
                { id:'sample3', name:'Aloo Tikki Burger', price:80, image_url:'images/burger1.jpeg', protein:10, carbs:52, fats:20, calories:430, category:'non-diet', description:'Tasty treat.' }
            ];
        }

        // Ensure image URLs are absolute paths
        foodItems.forEach(item => {
            if (!item.image_url.startsWith('/')) {
                item.image_url = '/static/' + item.image_url;
            }
        });

        // Filter based on preference
        const dietPreference = localStorage.getItem('dietPreference');
        if (dietPreference === 'diet') {
            foodItems = foodItems.filter(item => (item.category||'').toLowerCase() === 'diet');
        } else if (dietPreference === 'non-diet') {
            foodItems = foodItems.filter(item => (item.category||'').toLowerCase() === 'non-diet');
        }

        const menuGrid = document.querySelector('.menu-grid');
        if (!menuGrid) return;
        menuGrid.innerHTML = '';

        // Render cards
        foodItems.forEach((item, index) => {
            const menuItem = document.createElement('div');
            menuItem.className = 'menu-item menu-card';

            const chartId = `nutrition-chart-${index}`;

            menuItem.innerHTML = `
                <div class="image-block">
                    <img src="${item.image_url}" alt="${item.name}" class="item-image">
                </div>
                <div class="item-details">
                    <div class="title-rating">
                        <h3 class="item-title">${item.name}</h3>
                        <div class="item-rating">
                            <span class="star-icon">&#9733;</span> 4.5
                        </div>
                    </div>
                    <p class="item-description">${item.description || ''}</p>
                    <div class="nutrition-info">
                        <div class="nutrition-values">
                            <span class="nutrition-item">Protein: ${item.protein || 0}g</span>
                            <span class="nutrition-item">Carbs: ${item.carbs || 0}g</span>
                            <span class="nutrition-item">Fats: ${item.fats || 0}g</span>
                            <span class="nutrition-item">Calories: ${item.calories || 0}</span>
                        </div>
                        <div class="nutrition-chart">
                            <canvas id="${chartId}" width="100" height="100"></canvas>
                        </div>
                    </div>
                    <p class="item-price">₹${item.price}</p>
                    <div class="quantity-controls">
                        <button class="quantity-btn" onclick="decreaseQuantity('${item.id}')">-</button>
                        <span class="quantity-display" id="quantity-${item.id}">1</span>
                        <button class="quantity-btn" onclick="increaseQuantity('${item.id}')">+</button>
                    </div>
                    <button class="add-to-cart-btn" onclick="showAddToCartConfirmation('${item.id}', '${item.name}', '${item.price}', '${item.image_url}', '${item.protein}', '${item.carbs}', '${item.fats}', '${item.calories}')">Add to Cart</button>
                </div>
            `;

            menuGrid.appendChild(menuItem);
            setTimeout(() => {
                createNutritionChart(chartId, parseInt(item.protein||0), parseInt(item.carbs||0), parseInt(item.fats||0), parseInt(item.calories||0));
            }, 50);
        });

        updateCartCount();
    } catch (error) {
        console.error('Error loading food items (handled gracefully):', error);
    }
}

// Function to load cart page
function loadCartPage() {
    const cartItems = document.getElementById('cart-items');
    const cartSummary = document.getElementById('cart-summary');
    const emptyCart = document.getElementById('empty-cart');

    cart = JSON.parse(localStorage.getItem('cart')) || [];

    if (cart.length === 0) {
        cartItems.style.display = 'none';
        cartSummary.style.display = 'none';
        emptyCart.style.display = 'block';
        return;
    }

    emptyCart.style.display = 'none';
    cartItems.style.display = 'block';
    cartSummary.style.display = 'block';

    // Render cart items
    cartItems.innerHTML = cart.map(item => `
        <div class="cart-item">
            <img src="${item.image_url || '/static/images/default-food.jpg'}" alt="${item.name}" class="cart-item-image">
            <div class="cart-item-details">
                <h4>${item.name}</h4>
                <p>₹${item.price} each</p>
                <div class="cart-quantity-controls">
                    <button class="quantity-btn" onclick="updateCartQuantity('${item.id}', -1)">-</button>
                    <span class="quantity-display">${item.quantity}</span>
                    <button class="quantity-btn" onclick="updateCartQuantity('${item.id}', 1)">+</button>
                </div>
            </div>
            <div class="cart-item-total">
                <p>₹${(item.price * item.quantity).toFixed(2)}</p>
                <button class="remove-btn" onclick="removeFromCart('${item.id}')">Remove</button>
            </div>
        </div>
    `).join('');

    // Render cart summary with GST (18%)
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const subTotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const gst = subTotal * 0.18;
    const grandTotal = subTotal + gst;

    // Calculate nutritional totals
    const nutritionTotals = cart.reduce((acc, item) => {
        acc.protein += (item.protein || 0) * item.quantity;
        acc.carbs += (item.carbs || 0) * item.quantity;
        acc.fats += (item.fats || 0) * item.quantity;
        acc.calories += (item.calories || 0) * item.quantity;
        return acc;
    }, { protein: 0, carbs: 0, fats: 0, calories: 0 });

    const deliveryFee = 50;
    const finalTotal = subTotal + gst + deliveryFee;

    cartSummary.innerHTML = `
        <h3>Order Summary</h3>
        <div class="summary-row"><span>Subtotal</span><span>₹${subTotal.toFixed(2)}</span></div>
        <div class="summary-row"><span>GST (18%)</span><span>₹${gst.toFixed(2)}</span></div>
        <div class="summary-row"><span>Delivery Fee</span><span>₹${deliveryFee.toFixed(2)}</span></div>
        <div class="summary-row total"><span>Final Amount</span><span>₹${finalTotal.toFixed(2)}</span></div>
        <div class="nutrition-summary">
            <h4>Nutritional Summary</h4>
            <div class="nutrition-row"><span>Protein</span><span>${nutritionTotals.protein.toFixed(1)}g</span></div>
            <div class="nutrition-row"><span>Carbs</span><span>${nutritionTotals.carbs.toFixed(1)}g</span></div>
            <div class="nutrition-row"><span>Fats</span><span>${nutritionTotals.fats.toFixed(1)}g</span></div>
            <div class="nutrition-row"><span>Calories</span><span>${Math.round(nutritionTotals.calories)}</span></div>
        </div>
        <button class="checkout-btn" style="margin-bottom:10px;" onclick="placeOrder()">Place Order</button>
        <button class="checkout-btn" onclick="proceedToPayment()">Proceed to Payment</button>
        <div style="font-size:12px;color:#777;margin-top:6px;">Payment will be processed automatically • Secure checkout</div>
    `;

    updateCartCount();

    // Render nutrition analytics
    renderCartNutrition();
}

// Function to load cart count on all pages
function loadCartCount() {
    updateCartCount();
}

// Function to update cart quantity
function updateCartQuantity(itemId, change) {
    const item = cart.find(item => item.id == itemId);
    if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
            removeFromCart(itemId);
            return;
        }
        saveCart();
        loadCartPage();
    }
}

// Function to remove item from cart
function removeFromCart(itemId) {
    cart = cart.filter(item => item.id != itemId);
    saveCart();
    loadCartPage();
}

// Function to proceed to payment
function showProcessingOverlay() {
    // Avoid duplicating
    if (document.getElementById('processingOverlay')) return;
    const overlay = document.createElement('div');
    overlay.id = 'processingOverlay';
    overlay.style.position = 'fixed';
    overlay.style.inset = '0';
    overlay.style.background = 'rgba(0,0,0,0.35)';
    overlay.style.zIndex = '9999';
    overlay.style.display = 'flex';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';

    const card = document.createElement('div');
    card.style.background = '#fff';
    card.style.borderRadius = '14px';
    card.style.boxShadow = '0 10px 30px rgba(0,0,0,0.2)';
    card.style.width = '520px';
    card.style.maxWidth = '92%';
    card.style.padding = '26px';
    card.style.textAlign = 'center';

    card.innerHTML = `
        <div style="width:64px;height:64px;margin:0 auto 12px auto;border-radius:50%;background:#e6f4ea;display:flex;align-items:center;justify-content:center;font-size:26px;color:#2e7d32;">↗</div>
        <div style="font-weight:800;color:#7a3b41;font-size:20px;margin-bottom:6px;">Processing Your Order</div>
        <div style="color:#4b5563;margin-bottom:14px;">Generating your personalized diet plan...</div>
        <div style="height:8px;background:#eef2f7;border-radius:999px;overflow:hidden;">
            <div id="processingBar" style="height:100%;width:10%;background:#2e7d32;border-radius:999px;transition:width 0.25s ease;"></div>
        </div>
    `;
    overlay.appendChild(card);
    document.body.appendChild(overlay);

    // Animate bar
    let pct = 10;
    const timer = setInterval(() => {
        pct = Math.min(95, pct + Math.floor(Math.random()*15)+5);
        const bar = document.getElementById('processingBar');
        if (bar) bar.style.width = pct + '%';
    }, 250);

    return () => { clearInterval(timer); document.body.removeChild(overlay); };
}

function proceedToPayment() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || !user.id) {
        alert('Please login to continue to payment.');
        window.location.href = '/login';
        return;
    }

    // Ensure latest order is confirmed by admin before allowing payment
    fetch(`http://127.0.0.1:3000/user-orders/${user.id}`)
        .then(resp => resp.ok ? resp.json() : [])
        .then(orders => {
            if (!orders || !orders.length) {
                alert('You have no orders to pay for. Please place an order first.');
                return;
            }

            const latest = orders[0];
            if (latest.order_status === 'cancelled') {
                alert('Your latest order was cancelled by the admin. Please place a new order.');
                return;
            }

            if (latest.order_status !== 'confirmed') {
                alert('Your latest order is not yet confirmed by the admin. Please wait for confirmation before paying.');
                return;
            }

            localStorage.setItem('latestOrderId', latest.id);

            const hide = showProcessingOverlay();
            setTimeout(() => {
                hide && hide();
                window.location.href = '/payment';
            }, 1600);
        })
        .catch(() => {
            alert('Unable to check order status. Please try again.');
        });
}

// Function to load payment page
function loadPaymentPage() {
    const orderSummary = document.getElementById('order-summary');
    const guestDetails = document.getElementById('guest-details');
    cart = JSON.parse(localStorage.getItem('cart')) || [];

    if (cart.length === 0) {
        alert('Your cart is empty!');
        window.location.href = '/cart';
        return;
    }

    // Check if user is logged in
    const user = JSON.parse(localStorage.getItem('user')) || {};
    if (!user.name || !user.mobile || !user.email) {
        // Show guest details form
        guestDetails.style.display = 'block';
    } else {
        // Hide guest details form
        guestDetails.style.display = 'none';
    }

    const totalPrice = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const gst = totalPrice * 0.18;
    const deliveryFee = 50;
    const grandTotal = totalPrice + gst + deliveryFee;

    orderSummary.innerHTML = `
        <h3>Order Summary</h3>
        <div class="order-items">
            ${cart.map(item => `
                <div class="order-item">
                    <span>${item.name} x${item.quantity}</span>
                    <span>₹${(item.price * item.quantity).toFixed(2)}</span>
                </div>
            `).join('')}
        </div>
        <div class="order-total">
            <div class="summary-row">
                <span>Subtotal:</span>
                <span>₹${totalPrice.toFixed(2)}</span>
            </div>
            <div class="summary-row">
                <span>GST (18%):</span>
                <span>₹${gst.toFixed(2)}</span>
            </div>
            <div class="summary-row">
                <span>Delivery Fee:</span>
                <span>₹${deliveryFee.toFixed(2)}</span>
            </div>
            <div class="summary-row total">
                <span>Final Amount:</span>
                <span>₹${grandTotal.toFixed(2)}</span>
            </div>
        </div>
    `;

    updateCartCount();
}

// Function to toggle payment form based on selected method
function togglePaymentForm() {
    const selectedMethod = document.querySelector('input[name="paymentMethod"]:checked').value;
    const cardForm = document.getElementById('card-payment-form');
    const codPayment = document.getElementById('cod-payment');

    if (selectedMethod === 'card') {
        cardForm.style.display = 'block';
        codPayment.style.display = 'none';
    } else {
        cardForm.style.display = 'none';
        codPayment.style.display = 'block';
    }
}

// Function to process card payment
async function processCardPayment(event) {
    event.preventDefault();

    // Basic validation
    const cardNumber = document.getElementById('cardNumber').value;
    const expiryDate = document.getElementById('expiryDate').value;
    const cvv = document.getElementById('cvv').value;
    const cardName = document.getElementById('cardName').value;

    if (!cardNumber || !expiryDate || !cvv || !cardName) {
        alert('Please fill in all payment details.');
        return;
    }

    // Get user details
    const user = JSON.parse(localStorage.getItem('user')) || {};
    const totalAmount = calculateTotal();

    // Get guest details if not logged in
    let customerName = user.name;
    let customerMobile = user.mobile;
    let customerEmail = user.email;
    let dietPreference = null;

    if (!customerName || !customerMobile || !customerEmail) {
        customerName = document.getElementById('guestName').value;
        customerMobile = document.getElementById('guestMobile').value;
        customerEmail = document.getElementById('guestEmail').value;
        dietPreference = document.getElementById('dietPreference').value;

        if (!customerName || !customerMobile || !customerEmail) {
            alert('Please fill in guest details.');
            return;
        }
    }

    try {
        // Save order to database
        const saveResponse = await fetch('http://127.0.0.1:3000/save-order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: user.id || null,
                name: customerName,
                mobile: customerMobile,
                email: customerEmail,
                order_data: JSON.stringify(cart),
                total_amount: totalAmount,
                payment_method: 'Card Payment',
                diet_preference: dietPreference
            })
        });

        if (!saveResponse.ok) {
            throw new Error('Failed to save order');
        }

        // Generate and download invoice
        await generateAndDownloadInvoice('Card Payment', customerName, customerMobile);

        // Save order to localStorage for display
        await saveOrder('Paid', 'Card Payment');

        // Simulate payment processing
        alert('Card payment successful! Your order has been placed. Invoice downloaded.');

        // Clear cart
        localStorage.removeItem('cart');
        cart = [];

        // Redirect to orders
        window.location.href = '/orders';
    } catch (error) {
        alert('Error processing payment: ' + error.message);
    }
}

// Function to process cash on delivery
async function processCodPayment() {
    // Confirm COD order
    if (confirm('Confirm your Cash on Delivery order? You will pay ₹' + calculateTotal() + ' when the order is delivered.')) {
        // Get user details
        const user = JSON.parse(localStorage.getItem('user')) || {};
        const totalAmount = calculateTotal();

        // Get guest details if not logged in
        let customerName = user.name;
        let customerMobile = user.mobile;
        let customerEmail = user.email;
        let dietPreference = null;

        if (!customerName || !customerMobile || !customerEmail) {
            customerName = document.getElementById('guestName').value;
            customerMobile = document.getElementById('guestMobile').value;
            customerEmail = document.getElementById('guestEmail').value;
            dietPreference = document.getElementById('dietPreference').value;

            if (!customerName || !customerMobile || !customerEmail) {
                alert('Please fill in guest details.');
                return;
            }
        }

        try {
            // Save order to database
            const saveResponse = await fetch('http://127.0.0.1:3000/save-order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
            body: JSON.stringify({
                user_id: user.id || null,
                name: customerName,
                mobile: customerMobile,
                email: customerEmail,
                order_data: JSON.stringify(cart),
                total_amount: totalAmount,
                payment_method: 'Cash on Delivery',
                diet_preference: dietPreference
            })
            });

            if (!saveResponse.ok) {
                throw new Error('Failed to save order');
            }

            // Generate and download invoice
            await generateAndDownloadInvoice('Cash on Delivery', customerName, customerMobile);

            // Save order to localStorage for display
            await saveOrder('Paid', 'Cash on Delivery');

            alert('Cash on Delivery order confirmed! Your order will be delivered in 30-45 minutes. Invoice downloaded.');

            // Clear cart
            localStorage.removeItem('cart');
            cart = [];

            // Redirect to orders
            window.location.href = '/orders';
        } catch (error) {
            alert('Error processing COD order: ' + error.message);
        }
    }
}

// Function to generate and download invoice
async function generateAndDownloadInvoice(paymentMethod, customerName, customerMobile) {
    try {
        const response = await fetch('http://127.0.0.1:3000/generate-invoice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                orderItems: cart,
                totalAmount: calculateTotal(),
                paymentMethod: paymentMethod,
                customerName: customerName,
                customerMobile: customerMobile
            })
        });

        if (!response.ok) {
            throw new Error('Failed to generate invoice');
        }

        const data = await response.json();

        // Create a download link for the PDF
        const link = document.createElement('a');
        link.href = 'data:application/pdf;base64,' + data.pdf;
        link.download = `HangOut Cafe_Invoice_${data.invoiceNumber}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

    } catch (error) {
        console.error('Error generating invoice:', error);
        alert('Failed to generate invoice. Please try again.');
    }
}

// Helper function to calculate total
function calculateTotal() {
    cart = JSON.parse(localStorage.getItem('cart')) || [];
    const totalPrice = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const gst = totalPrice * 0.18;
    const deliveryFee = 50;
    return (totalPrice + gst + deliveryFee).toFixed(2);
}

// -------- Orders Storage & Rendering --------
async function saveOrder(status, paymentMethod) {
    const user = JSON.parse(localStorage.getItem('user')) || {};
    const existing = JSON.parse(localStorage.getItem('orders') || '[]');

    const orderNumber = '#'+Math.floor(Math.random()*1e10).toString(16);
    const totals = cart.reduce((acc, it) => {
        acc.itemsTotal += it.price * it.quantity;
        acc.protein += (it.protein||0) * it.quantity;
        acc.carbs += (it.carbs||0) * it.quantity;
        acc.fats += (it.fats||0) * it.quantity;
        acc.calories += (it.calories||0) * it.quantity;
        return acc;
    }, { itemsTotal:0, protein:0, carbs:0, fats:0, calories:0 });

    const order = {
        id: orderNumber,
        date: new Date().toISOString(),
        status: status,
        paymentMethod,
        items: cart.map(i => ({ name: i.name, quantity: i.quantity, price: i.price })),
        metrics: totals,
        total: (totals.itemsTotal + 50) // add delivery like payment page
    };

    existing.unshift(order);
    localStorage.setItem('orders', JSON.stringify(existing));
}

let globalFoodItems = [];

async function loadOrdersPage() {
    const list = document.getElementById('orders-list');
    const empty = document.getElementById('orders-empty');

    const orders = JSON.parse(localStorage.getItem('orders') || '[]');
    if (!orders.length) {
        if (empty) empty.style.display = 'block';
        return;
    }
    if (empty) empty.style.display = 'none';

    if (!list) return;

    // Load food items for add to cart functionality
    try {
        const response = await fetch('http://127.0.0.1:3000/food-items');
        if (response.ok) {
            globalFoodItems = await response.json();
        }
    } catch (e) {
        console.error('Error loading food items for orders:', e);
    }

    list.innerHTML = orders.map((o, index) => `
        <div class="order-card">
            <div class="order-bar">
                <div>Order ${o.id}<div style="font-size:12px;color:#7a8188;">${new Date(o.date).toLocaleDateString()}</div></div>
                <span class="order-status">${o.status}</span>
            </div>
            <div class="order-body">
                <div class="order-items-list">${o.items.map(it => `${it.name} x${it.quantity}`).join('<br>')}</div>
                <div class="order-metrics">
                    <div class="metric-box"><h5>Protein</h5><div class="metric-val">${o.metrics.protein.toFixed(1)}g</div></div>
                    <div class="metric-box"><h5>Carbs</h5><div class="metric-val">${o.metrics.carbs.toFixed(1)}g</div></div>
                    <div class="metric-box"><h5>Fats</h5><div class="metric-val">${o.metrics.fats.toFixed(1)}g</div></div>
                    <div class="metric-box"><h5>Calories</h5><div class="metric-val">${Math.round(o.metrics.calories)}</div></div>
                    <div class="metric-box"><h5>Total</h5><div class="metric-val">₹${o.total.toFixed(2)}</div></div>
                </div>
            </div>
            <div class="order-footer">
                <button class="invoice-btn" onclick="alert('Invoice already downloaded during checkout.')">View Invoice</button>
                <button class="delete-order-btn" onclick="deleteOrder(${index})" style="margin-left:10px; background:#e74c3c; color:white; border:none; padding:4px 8px; border-radius:4px; cursor:pointer; font-size:12px;">Delete Order</button>
                <button class="add-to-cart-btn" onclick="addOrderToCart(${index})" style="margin-left:10px; font-size:12px; padding:4px 8px;">Add to Cart</button>
            </div>
        </div>
    `).join('');
}

function addOrderToCart(orderIndex) {
    const orders = JSON.parse(localStorage.getItem('orders') || '[]');
    const order = orders[orderIndex];
    if (!order) return;

    if (confirm(`Add the entire order ${order.id} to cart?`)) {
        let addedCount = 0;
        order.items.forEach(item => {
            const fullItem = globalFoodItems.find(fi => fi.name === item.name);
            if (fullItem) {
                for (let i = 0; i < item.quantity; i++) {
                    addToCart(fullItem.id, fullItem.name, fullItem.price, fullItem.image_url, fullItem.protein, fullItem.carbs, fullItem.fats, fullItem.calories);
                }
                addedCount += item.quantity;
            } else {
                alert(`Item "${item.name}" not found in current menu.`);
            }
        });
        if (addedCount > 0) {
            alert(`${addedCount} item(s) from order ${order.id} added to cart!`);
        }
    }
}

function deleteOrder(orderIndex) {
    const orders = JSON.parse(localStorage.getItem('orders') || '[]');
    const order = orders[orderIndex];
    if (!order) return;

    if (confirm(`Are you sure you want to delete order ${order.id}? This action cannot be undone.`)) {
        orders.splice(orderIndex, 1);
        localStorage.setItem('orders', JSON.stringify(orders));
        alert(`Order ${order.id} has been deleted.`);
        loadOrdersPage(); // Reload the orders page to reflect the changes
    }
}

// --- Cart nutrition rendering ---
function renderCartNutrition() {
    const section = document.getElementById('nutrition-section');
    if (!section) return;

    cart = JSON.parse(localStorage.getItem('cart')) || [];
    if (cart.length === 0) {
        section.style.display = 'none';
        return;
    }

    const totals = cart.reduce((acc, item) => {
        acc.protein += (item.protein || 0) * item.quantity;
        acc.carbs += (item.carbs || 0) * item.quantity;
        acc.fats += (item.fats || 0) * item.quantity;
        acc.calories += (item.calories || 0) * item.quantity;
        return acc;
    }, { protein: 0, carbs: 0, fats: 0, calories: 0 });

    section.style.display = 'block';

    const cards = document.getElementById('nutrition-cards');
    if (cards) {
        cards.innerHTML = `
            <div class="nutrition-card"><h4>Protein</h4><div class="nutrition-value">${totals.protein.toFixed(1)}g</div></div>
            <div class="nutrition-card"><h4>Carbs</h4><div class="nutrition-value">${totals.carbs.toFixed(1)}g</div></div>
            <div class="nutrition-card"><h4>Fats</h4><div class="nutrition-value">${totals.fats.toFixed(1)}g</div></div>
            <div class="nutrition-card"><h4>Calories</h4><div class="nutrition-value">${Math.round(totals.calories)}</div></div>
        `;
    }

    // Draw charts
    const pieCanvas = document.getElementById('macroPieChart');
    const barCanvas = document.getElementById('macroBarChart');
    if (pieCanvas) {
        new Chart(pieCanvas, {
            type: 'pie',
            data: {
                labels: ['Protein', 'Carbs', 'Fats'],
                datasets: [{
                    data: [totals.protein, totals.carbs, totals.fats],
                    backgroundColor: ['#2e7d32', '#7a3b41', '#f39c12']
                }]
            },
            options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
        });
    }
    if (barCanvas) {
        new Chart(barCanvas, {
            type: 'bar',
            data: {
                labels: ['Protein', 'Carbs', 'Fats'],
                datasets: [{
                    label: 'Macronutrient Grams',
                    data: [totals.protein, totals.carbs, totals.fats],
                    backgroundColor: ['#2e7d32', '#7a3b41', '#f39c12']
                }]
            },
            options: { responsive: true, scales: { y: { beginAtZero: true } } }
        });
    }
}

// --- CSV helper (quoted fields + multi-filename support) ---
function csvSafeSplit(line) {
    const parts = [];
    let cur = '';
    let inQ = false;
    for (let i = 0; i < line.length; i++) {
        const ch = line[i];
        if (ch === '"') {
            if (inQ && line[i+1] === '"') { cur += '"'; i++; }
            else { inQ = !inQ; }
        } else if (ch === ',' && !inQ) {
            parts.push(cur.trim()); cur = '';
        } else { cur += ch; }
    }
    parts.push(cur.trim());
    return parts.map(v => v.replace(/^"|"$/g, ''));
}

async function loadItemsFromCsv(csvPath) {
    try {
        const res = await fetch(csvPath, { cache: 'no-store' });
        if (!res.ok) return null;
        const text = await res.text();
        const lines = text.split(/\r?\n/).filter(l => l.trim().length > 0);
        if (lines.length < 2) return null;
        const headers = csvSafeSplit(lines[0]).map(h => h.trim());
        const rows = lines.slice(1).map(line => {
            const cols = csvSafeSplit(line);
            const obj = {};
            headers.forEach((h, i) => obj[h] = (cols[i] || '').trim());
            return obj;
        });
        return rows.map(r => ({
            id: r.id || r.ID || r.slug || r.name,
            name: r.name || r.title,
            description: r.description || r.desc || '',
            price: parseFloat(r.price || r.cost || 0),
            image_url: r.image_url || r.image || r.photo || r.imageUrl || '',
            protein: parseFloat(r.protein || r.proteins || 0),
            carbs: parseFloat(r.carbs || r.carb || 0),
            fats: parseFloat(r.fats || r.fat || 0),
            calories: parseFloat(r.calories || r.kcal || 0),
            category: (r.category || r.type || '').toLowerCase()
        }));
    } catch (_) {
        return null;
    }
}

async function loadItemsFromCsvPaths(paths) {
    for (const p of paths) {
        const items = await loadItemsFromCsv(p);
        if (items && items.length) return items;
    }
    return null;
}

// --- AI Recommendations ---
async function loadAIRecommendations() {
    const body = document.getElementById('aiRecoBody');
    const cardsContainer = document.getElementById('aiRecoCards');
    const loading = document.getElementById('aiRecoLoading');
    const tag = document.getElementById('aiRecoTag');
    if (!body || !cardsContainer) return;

    loading.style.display = 'block';
    cardsContainer.style.display = 'none';

    try {
        // Backend first (original behavior)
        let items = [];
        try {
            const res = await fetch('http://127.0.0.1:3000/food-items');
            if (res.ok) {
                items = await res.json();
                try { localStorage.setItem('cachedFoodItems', JSON.stringify(items)); } catch (_) {}
            }
        } catch (_) { /* ignore */ }
        // CSV fallback
        if (!items || items.length === 0) {
            items = await loadItemsFromCsvPaths(['FoodItem_export_clean.csv', 'fooditem_export.csv','item_export.csv']);
        }
        if (!items || items.length === 0) {
            const cached = JSON.parse(localStorage.getItem('cachedFoodItems') || '[]');
            if (cached.length) items = cached;
        }
        if (!items || items.length === 0) {
            // built-in minimal sample so UI never looks empty
            items = [
                { id:'sample1', name:'Sprouts Chaat', price:110, image_url:'images/pizza1.jpeg', protein:18, carbs:28, fats:6, calories:230, category:'diet', description:'Light and protein rich.' },
                { id:'sample2', name:'Paneer Tikka', price:280, image_url:'images/indian.jpeg', protein:24, carbs:45, fats:28, calories:550, category:'diet', description:'Creamy classic.' },
                { id:'sample3', name:'Aloo Tikki Burger', price:80, image_url:'images/burger1.jpeg', protein:10, carbs:52, fats:20, calories:430, category:'non-diet', description:'Tasty treat.' }
            ];
        }
        const pref = localStorage.getItem('dietPreference');
        tag.textContent = pref === 'diet' ? 'Diet picks' : (pref === 'non-diet' ? 'Treat yourself' : 'Balanced');

        // Simple heuristic: Diet -> high protein, Non-diet -> high calories, else top rating proxy by carbs
        if (pref === 'diet') {
            items.sort((a,b) => (parseFloat(b.protein||0)) - (parseFloat(a.protein||0)));
        } else if (pref === 'non-diet') {
            items.sort((a,b) => (parseFloat(b.calories||0)) - (parseFloat(a.calories||0)));
        } else {
            items.sort((a,b) => (parseFloat(b.carbs||0)) - (parseFloat(a.carbs||0)));
        }

        const top = items.slice(0, 5);
        // Ensure image URLs are absolute paths
        top.forEach(it => {
            if (!it.image_url.startsWith('/')) {
                it.image_url = '/static/' + it.image_url;
            }
        });
        cardsContainer.innerHTML = top.map(it => `
            <div class="ai-card">
                <img src="${it.image_url}" alt="${it.name}">
                <div class="ai-card-body">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <strong>${it.name}</strong>
                        <span class="item-price" style="margin:0">₹${it.price}</span>
                    </div>
                    <button class="add-to-cart-btn" style="margin-top:8px" onclick="showAddToCartConfirmation('${it.id}','${it.name}','${it.price}','${it.image_url}','${it.protein}','${it.carbs}','${it.fats}','${it.calories}')">Add to Cart</button>
                </div>
            </div>
        `).join('');

        // brief delay to show analyzing
        setTimeout(() => {
            loading.style.display = 'none';
            cardsContainer.style.display = 'grid';
        }, 700);
    } catch(e) {
        loading.textContent = 'Unable to load recommendations.';
    }
}

// Existing DOMContentLoaded logic
document.addEventListener('DOMContentLoaded', () => {
    // Check the URL to only run loadProfile on the profile page
    if (window.location.pathname.includes('profile')) {
        // Check if user is logged in
        const user = JSON.parse(localStorage.getItem('user'));
        if (!user) {
            alert('Please login first!');
            window.location.href = '/login';
            return;
        }
        loadProfile();
        renderProfileInsights();
    }

    // Load food items on cafeteria page
    if (window.location.pathname.includes('cafeteria')) {
    // Show welcome popup
    const welcomePopup = document.getElementById('welcomePopup');
    const continueBtn = document.getElementById('continueBtn');

    if (welcomePopup && continueBtn) {
        welcomePopup.style.display = 'flex';

        // Handle continue button to show intermediate popup
        continueBtn.addEventListener('click', () => {
            welcomePopup.style.display = 'none';
            showIntermediatePopup();
        });
    }

        // Render AI recommendations banner
        loadAIRecommendations();

        // Filter chip events
        const filterAll = document.getElementById('filterAll');
        const filterDiet = document.getElementById('filterDiet');
        const filterNon = document.getElementById('filterNonDiet');
        const setActive = (el) => {
            [filterAll, filterDiet, filterNon].forEach(b => b && b.classList.remove('active'));
            el && el.classList.add('active');
        };
        filterAll && filterAll.addEventListener('click', () => { localStorage.removeItem('dietPreference'); setActive(filterAll); loadFoodItems(); loadAIRecommendations(); });
        filterDiet && filterDiet.addEventListener('click', () => { localStorage.setItem('dietPreference','diet'); setActive(filterDiet); loadFoodItems(); loadAIRecommendations(); });
        filterNon && filterNon.addEventListener('click', () => { localStorage.setItem('dietPreference','non-diet'); setActive(filterNon); loadFoodItems(); loadAIRecommendations(); });
    }

    // Load cart page
    if (window.location.pathname.includes('/cart')) {
        loadCartPage();
    }

    // Load payment page
    if (window.location.pathname.includes('/payment')) {
        loadPaymentPage();
    }

    // Load orders page
    if (window.location.pathname.includes('/orders')) {
        loadOrders();
    }

    // Load cart count on all pages
    loadCartCount();

    // Attempt AI recos on any page that contains the section
    loadAIRecommendations();

    // NEW: Check if the login page is being loaded and handle URL hash
    // This allows linking to the register form directly or handling browser back/forward
    if (window.location.pathname.includes('login.html') && window.location.hash === '#register') {
        showRegisterPanel();
    }

    // Add event listener to OTP input to handle Enter key
    const otpInput = document.getElementById('otpInput');
    if (otpInput) {
        otpInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                verifyOtp();
            }
        });
    }
});

// Function to clear all orders
function clearAllOrders() {
    if (confirm('Are you sure you want to clear all orders? This action cannot be undone.')) {
        localStorage.removeItem('orders');
        alert('All orders have been cleared.');
        loadOrdersPage(); // Reload the orders page to show empty state
    }
}

// Function to load login history
async function loadLoginHistory() {
    const user = JSON.parse(localStorage.getItem('user')) || {};
    const container = document.getElementById('loginHistoryContainer');

    if (!container || !user.mobile) return;

    try {
        const response = await fetch('http://127.0.0.1:3000/get-login-history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mobile: user.mobile })
        });

        if (response.ok) {
            const data = await response.json();
            const history = data.loginHistory || [];

            if (history.length === 0) {
                container.innerHTML = '<div style="text-align: center; color: #6b7b88; padding: 20px;">No login history available</div>';
                return;
            }

            const historyHTML = history.map(entry => {
                const loginTime = new Date(entry.login_time);
                const formattedTime = loginTime.toLocaleString('en-IN', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: true
                });
                return `
                    <div style="border-bottom: 1px solid #e0e0e0; padding: 8px 0; font-size: 12px; color: #4b5563;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span>${formattedTime}</span>
                            <span style="color: #6b7b88;">Login #${entry.id}</span>
                        </div>
                    </div>
                `;
            }).join('');

            container.innerHTML = historyHTML;
        } else {
            container.innerHTML = '<div style="text-align: center; color: #6b7b88; padding: 20px;">Unable to load login history</div>';
        }
    } catch (error) {
        console.error('Error fetching login history:', error);
        container.innerHTML = '<div style="text-align: center; color: #6b7b88; padding: 20px;">Error loading login history</div>';
    }
}

// Function to render profile insights and statistics
async function renderProfileInsights() {
    const user = JSON.parse(localStorage.getItem('user')) || {};
    if (!user.mobile) return;

    try {
        // Fetch login count
        const loginResponse = await fetch('http://127.0.0.1:3000/login-count', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: user.email })
        });
        if (loginResponse.ok) {
            const loginData = await loginResponse.json();
            document.getElementById('totalLogins').textContent = loginData.loginCount || 0;
        }

        // Fetch login history
        loadLoginHistory();

        // Fetch user orders for statistics
        const ordersResponse = await fetch('http://127.0.0.1:3000/get-guest-orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mobile: user.mobile, email: user.email })
        });
        if (ordersResponse.ok) {
            const ordersData = await ordersResponse.json();
            const orders = ordersData.orders || [];
            document.getElementById('totalOrdersCount').textContent = orders.length;

            // Calculate nutritional insights
            if (orders.length > 0) {
                let totalProtein = 0, totalCarbs = 0, totalFats = 0, totalCalories = 0;
                let orderCount = 0;

                orders.forEach(order => {
                    try {
                        const items = JSON.parse(order.order_data);
                        items.forEach(item => {
                            totalProtein += (item.protein || 0) * item.quantity;
                            totalCarbs += (item.carbs || 0) * item.quantity;
                            totalFats += (item.fats || 0) * item.quantity;
                            totalCalories += (item.calories || 0) * item.quantity;
                        });
                        orderCount++;
                    } catch (e) {
                        console.error('Error parsing order data:', e);
                    }
                });

                if (orderCount > 0) {
                    document.getElementById('avgProtein').textContent = (totalProtein / orderCount).toFixed(1) + 'g';
                    document.getElementById('avgCarbs').textContent = (totalCarbs / orderCount).toFixed(1) + 'g';
                    document.getElementById('avgFats').textContent = (totalFats / orderCount).toFixed(1) + 'g';
                    document.getElementById('avgCalories').textContent = Math.round(totalCalories / orderCount);
                }
            }

            // Determine preference based on orders
            const dietOrders = orders.filter(o => o.diet_preference === 'diet').length;
            const nonDietOrders = orders.filter(o => o.diet_preference === 'non-diet').length;
            if (dietOrders > nonDietOrders) {
                document.getElementById('prefText').textContent = 'Diet';
            } else if (nonDietOrders > dietOrders) {
                document.getElementById('prefText').textContent = 'Non-Diet';
            } else {
                document.getElementById('prefText').textContent = 'Mixed';
            }
        }
    } catch (error) {
        console.error('Error loading profile insights:', error);
    }
}

// Function to toggle between view and edit modes
function toggleEditMode() {
    const table = document.querySelector('.profile-table');
    const editBtn = document.querySelector('.edit-profile-btn');
    const form = document.getElementById('profileForm');

    if (!table || !editBtn || !form) return;

    // Check current display state
    const isFormVisible = form.style.display === 'block';
    
    if (isFormVisible) {
        // Switch to view mode (hide form, show table and button)
        table.style.display = 'table';
        editBtn.style.display = 'inline-block';
        form.style.display = 'none';
        // Reload profile data to show original info
        loadProfile();
    } else {
        // Switch to edit mode (hide table, show form)
        table.style.display = 'none';
        editBtn.style.display = 'none';
        form.style.display = 'block';
    }
}

// Function to place order using the new create-order API
async function placeOrder() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    const user = JSON.parse(localStorage.getItem("user"));

    if (!user || !user.id) {
        alert('Please login to place an order');
        window.location.href = '/login';
        return;
    }

    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }

    const response = await fetch("http://127.0.0.1:3000/create-order", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: user.id,
            cart: cart
        })
    });

    const data = await response.json();

    if (data.success) {
        alert("Order placed successfully! Your order is now pending admin approval.");
        // keep cart so user can pay after confirmation
        // optionally store latest order id
        localStorage.setItem("latestOrderId", data.order_id);
    } else {
        alert("Error: " + (data.error || "Failed to place order"));
    }
}

// Function to load user orders from database
async function loadUserOrders() {
    const user = JSON.parse(localStorage.getItem("user"));
    
    if (!user || !user.id) {
        console.log("User not logged in, skipping database orders fetch");
        return;
    }

    try {
        const response = await fetch(`/user-orders/${user.id}`);
        if (response.ok) {
            const dbOrders = await response.json();
            console.log("Orders from database:", dbOrders);
            // Store in localStorage for display
            if (dbOrders && dbOrders.length > 0) {
                const existingOrders = JSON.parse(localStorage.getItem('orders') || '[]');
                // Merge with existing local orders (avoid duplicates)
                const mergedOrders = [...dbOrders.map(o => ({
                    id: o.id,
                    date: o.created_at,
                    status: o.order_status,
                    paymentMethod: 'Online',
                    items: [], // Items would need separate fetch
                    metrics: { protein: 0, carbs: 0, fats: 0, calories: 0 },
                    total: parseFloat(o.total_amount)
                })), ...existingOrders];
                localStorage.setItem('orders', JSON.stringify(mergedOrders));
            }
        }
    } catch (error) {
        console.error("Error fetching user orders from database:", error);
    }
}

async function loadOrders() {
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user || !user.id) {
        console.log("User not logged in, loading local orders only");
        loadOrdersPage();
        return;
    }

    try {
        // Fetch DB orders
        const dbResponse = await fetch(`http://127.0.0.1:3000/user-orders/${user.id}`);
        const dbOrders = dbResponse.ok ? await dbResponse.json() : [];

        // Fetch guest orders  
        const guestResponse = await fetch('http://127.0.0.1:3000/get-guest-orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                mobile: user.mobile || '', 
                email: user.email || '' 
            })
        });
        const guestData = guestResponse.ok ? await guestResponse.json() : { orders: [] };
        const guestOrders = guestData.orders || [];

        // Merge: DB first (server orders), then guest/local
        const allOrders = [
            ...dbOrders.map(o => ({
                id: `#DB${o.id}`,
                date: o.created_at,
                status: o.order_status || 'completed', 
                paymentMethod: 'Online',
                items: [], // Would need separate API call
                metrics: { protein: 0, carbs: 0, fats: 0, calories: 0 },
                total: parseFloat(o.total_amount || 0)
            })),
            ...guestOrders.map(o => ({
                id: `#G${o.id}`,
                date: o.order_date,
                status: 'completed',
                paymentMethod: o.payment_method,
                items: [],
                metrics: { protein: 0, carbs: 0, fats: 0, calories: 0 },
                total: parseFloat(o.total_amount)
            }))
        ];

        // Load localStorage orders too
        const localOrders = JSON.parse(localStorage.getItem('orders') || '[]');
        allOrders.push(...localOrders);

        // Sort by date desc
        allOrders.sort((a,b) => new Date(b.date) - new Date(a.date));

        // Update localStorage
        localStorage.setItem('orders', JSON.stringify(allOrders));

        // Render
        loadOrdersPage();

    } catch (error) {
        console.error("Error loading orders:", error);
        // Fallback to local orders
        loadOrdersPage();
    }
}