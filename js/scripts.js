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

    // Allow "Enter" key to send messages
    document.getElementById("user-input").addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevent accidental form submission
            sendMessage();
        }
    });

    // Attach click event to the new button
    document.getElementById("send-button").addEventListener("click", sendMessage);
});

// Function to handle sending messages
async function sendMessage() {
    const userInputField = document.getElementById("user-input");
    const userInput = userInputField.value.trim();

    if (!userInput) {
        alert("Please enter a question.");
        return;
    }

    // Clear the input after sending
    userInputField.value = "";

    // Display the user's message in the chat
    addMessageToChat("You", userInput);

    try {
        // Send a POST request to your Heroku app
        const response = await fetch("https://parhamweb-b1f70f7c7e89.herokuapp.com/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: userInput })
        });

        if (response.ok) {
            const data = await response.json();
            addMessageToChat("Bot", data.answer);
        } else {
            addMessageToChat("Bot", "Sorry, something went wrong. Please try again.");
        }
    } catch (error) {
        console.error("Error:", error);
        addMessageToChat("Bot", "There was an error connecting to the server.");
    }
}

// Function to add messages to the chat box
function addMessageToChat(sender, message) {
    const chatMessages = document.getElementById("chat-messages");
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");

    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatMessages.appendChild(messageElement);

    // Scroll to the latest message
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
