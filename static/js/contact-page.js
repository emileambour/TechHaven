document.addEventListener("DOMContentLoaded", function () {
    const contactForm = document.getElementById("contactForm");

    contactForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const message = document.getElementById("message").value;
        const formMessage = document.getElementById("formMessage");

        if (name && email && message) {
            formMessage.textContent = "Message sent successfully!";
            formMessage.style.color = "green";

            // Reset the form
            contactForm.reset();
        } else {
            formMessage.textContent = "Please fill in all fields.";
            formMessage.style.color = "red";
        }
    });

    // Initialize map with coordinates
    var map = L.map('map').setView([37.7749, -122.4194], 13); // San Francisco example

    // Load OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Add a marker at the location
    L.marker([37.7749, -122.4194]).addTo(map)
        .bindPopup('Our Location')
        .openPopup();
});
