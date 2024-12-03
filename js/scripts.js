document.addEventListener("DOMContentLoaded", function () {
    const collapsibleLinks = document.querySelectorAll(".menu .collapsible");

    collapsibleLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();

            // Toggle active class for clicked link
            link.classList.toggle("active");

            // Find and toggle submenu visibility
            const submenu = link.nextElementSibling;
            if (submenu) {
                submenu.style.display = submenu.style.display === "block" ? "none" : "block";
            }
        });
    });
});
