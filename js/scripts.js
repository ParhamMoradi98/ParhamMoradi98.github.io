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

async function sendMessage() {
  const userInput = document.getElementById("user-input").value;

  if (!userInput.trim()) {
      alert("Please enter a question.");
      return;
  }

  // Clear the input after sending
  document.getElementById("user-input").value = "";

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

function addMessageToChat(sender, message) {
  const chatMessages = document.getElementById("chat-messages");
  const messageElement = document.createElement("div");
  messageElement.classList.add("message");

  messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
  chatMessages.appendChild(messageElement);

  // Scroll to the latest message
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

  