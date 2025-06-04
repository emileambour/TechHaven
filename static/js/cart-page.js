
document.addEventListener("DOMContentLoaded", function () {
    // Clear cart functionality (server-side)
    const clearBtn = document.getElementById("clearCartBtn");
    if (clearBtn) {
        clearBtn.addEventListener("click", function () {
            fetch("/clear-cart", { method: "POST" })
                .then(res => res.json())
                .then(() => location.reload());
        });
    }

    
    // Checkout button functionality
    const checkoutBtn = document.getElementById("checkoutBtn");
    if (checkoutBtn) {
        checkoutBtn.addEventListener("click", function () {
            fetch("/checkout", { method: "POST" })
                .then(res => res.json())
                .then(() => {
                    alert("✅ Purchase successful!");
                    location.reload();
                });
        });
    }


    // Scroll to top button
    const scrollToTopBtn = document.getElementById("scrollToTopBtn");
    if (scrollToTopBtn) {
        window.addEventListener("scroll", function () {
            scrollToTopBtn.style.display = window.scrollY > 150 ? "block" : "none";
        });

        scrollToTopBtn.addEventListener("click", function () {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }
});
