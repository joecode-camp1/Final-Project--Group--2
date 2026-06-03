// app/static/js/splash.js

function handleAppInitialization() {
    const preloaderLayer = document.getElementById("preloader");
    const mainContentLayer = document.getElementById("main-content");
    
    // --- 1. PRELOADER HANDLING SECTION ---
    // This will only execute if the elements actually exist on the current page view
    if (preloaderLayer && mainContentLayer) {
        preloaderLayer.classList.add("opacity-0");
        mainContentLayer.classList.remove("opacity-0");
        mainContentLayer.classList.add("opacity-100");
        
        setTimeout(() => {
            preloaderLayer.style.display = "none";
        }, 700);
    }

    // --- 2. PASSWORD VISIBILITY SYSTEM ---
    // This runs independently so it works across your whole application layout
    const togglePasswordBtn = document.getElementById("toggle-password");
    const passwordInput = document.getElementById("password");

    if (togglePasswordBtn && passwordInput) {
        togglePasswordBtn.addEventListener("click", function() {
            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                togglePasswordBtn.textContent = "👁️"; 
                togglePasswordBtn.classList.remove("opacity-40");
                togglePasswordBtn.classList.add("text-blue-400", "opacity-100");
            } else {
                passwordInput.type = "password";
                togglePasswordBtn.textContent = "🔒"; 
                togglePasswordBtn.classList.remove("text-blue-400", "opacity-100");
                togglePasswordBtn.classList.add("opacity-40");
            }
        });
    }
}

// Bind initialization to global window loading execution hook
window.addEventListener("load", handleAppInitialization);