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

document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
  
    // Send a message when the user clicks the 'Send' button
    document.querySelector("button").addEventListener('click', function() {
      const question = userInput.value.trim();
  
      // If the question is empty, don't send
      if (question) {
        // Display the question in the chat window
        displayMessage('You', question);
  
        // Send the question to Flask backend
        fetch('http://localhost:5000/ask', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question: question }),
        })
        .then(response => response.json())
        .then(data => {
          // Display the answer in the chat window
          displayMessage('Bot', data.answer);
        })
        .catch(error => {
          console.error('Error:', error);
          displayMessage('Bot', 'Sorry, something went wrong. Please try again.');
        });
      }
  
      // Clear the input field
      userInput.value = '';
    });
  
    // Function to display the messages in the chat window
    function displayMessage(sender, message) {
      const messageDiv = document.createElement('div');
      messageDiv.classList.add('message');
      messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
      chatMessages.appendChild(messageDiv);
      chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the bottom
    }
  });
  