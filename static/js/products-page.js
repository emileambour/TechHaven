
document.addEventListener("DOMContentLoaded", function () {
    // Attach event listeners to all Add to Cart buttons
    const buttons = document.querySelectorAll(".add-to-cart");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            const productCard = this.closest(".product");
            const productId = productCard.getAttribute("data-id");

            fetch("/add-to-cart", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    id: parseInt(productId),
                    quantity: 1
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    alert("✅ Product added to cart!");
                } else {
                    alert("❌ Error: " + data.message);
                }
            })
            .catch(err => {
                alert("❌ Failed to add to cart.");
                console.error(err);
            });
        });
    });

    // Scroll to Top Button
    const scrollToTopBtn = document.getElementById("scrollToTopBtn");

    window.addEventListener("scroll", function () {
        scrollToTopBtn.style.display = window.scrollY > 150 ? "block" : "none";
    });

    scrollToTopBtn.addEventListener("click", function () {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });
});
