document.addEventListener("DOMContentLoaded", function() {

    // Highlight active page in the navbar
    const currentLocation = window.location.href;
    const menuItems = document.querySelectorAll("nav ul li a");

    menuItems.forEach(item => {
        if (item.href === currentLocation) {
            item.style.fontWeight = "bold";
            item.style.textDecoration = "underline";
        }
    });

    // Smooth scrolling for internal links
    document.querySelectorAll('nav ul li a').forEach(anchor => {
        anchor.addEventListener('click', function(event) {
            if (this.getAttribute("href").startsWith("#")) {
                event.preventDefault();
                const targetId = this.getAttribute("href").substring(1);
                const targetElement = document.getElementById(targetId);

                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 50,
                        behavior: "smooth"
                    });
                }
            }
        });
    });

    // Featured Products - Dynamic Generation
    const products = [
        { name: "iPhone 16", price: "$799", image: "../images/iPhone16.png" },
        { name: "Apple Watch Ultra", price: "$249", image: "../images/Apple Watch Ultra.png" },
        { name: "Logitech Doorbell", price: "$199", image: "../images/Logitech Doorbell.png" },
        { name: "PS5 Controller", price: "$75", image: "../images/PS5 Controller.png" }
    ];

    const productContainer = document.getElementById("product-list");

    products.forEach(product => {
        let productElement = document.createElement("div");
        productElement.classList.add("product");

        productElement.innerHTML = `
            <img src="${product.image}" alt="${product.name}">
            <p>${product.name} - ${product.price}</p>
        `;

        productContainer.appendChild(productElement);
    });

    // Scroll to Top Button
    const scrollToTopBtn = document.getElementById("scrollToTopBtn");

    window.addEventListener("scroll", function () {
        if (window.scrollY > 150) {
            scrollToTopBtn.style.display = "block";
        } else {
            scrollToTopBtn.style.display = "none";
        }
    });

    scrollToTopBtn.addEventListener("click", function () {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });
});
