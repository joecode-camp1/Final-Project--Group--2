
    // Handles the smooth micro-interaction exit animation
    function dismissToast(toastId) {
        const toast = document.getElementById(toastId);
        if (toast) {
            toast.classList.add('opacity-0', 'scale-95', '-translate-y-2');
            setTimeout(() => {
                toast.remove();
            }, 300);
        }
    }
    
    // Auto-dismiss success flash messages after 6 seconds natively
    document.addEventListener("DOMContentLoaded", () => {
        // Find all toast alerts on the page using a generic attribute query
        const alerts = document.querySelectorAll('[id^="flash-toast-"]');
        
        alerts.forEach((toast) => {
            // Check if the toast element contains green success style identifiers
            if (toast.classList.contains('bg-emerald-950/40')) {
                setTimeout(() => {
                    dismissToast(toast.id);
                }, 6000);
            }
        });
    });