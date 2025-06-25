function createWebSocket() {
  const chatContainer = document.getElementById("chat-container");
  if (!chatContainer) return; // Exit if chat container not found

  // Retrieve Django-passed variables from data attributes
  const roomName = chatContainer.dataset.roomName;

  if (roomName === "None") {
    return;
  }

  // Check if socket exists and is OPEN or CONNECTING
  if (
    window.chatSocket &&
    (window.chatSocket.readyState === WebSocket.OPEN ||
      window.chatSocket.readyState === WebSocket.CONNECTING)
  ) {
    return;
  }

  // // Initialize WebSocket connection
  const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
  const chatSocket = new WebSocket(
    `${protocol}${window.location.host}/ws/chats/${roomName}/`,
  );
  console.log(
    `Connection Established to ${protocol}${window.location.host}/ws/chats/${roomName}/`,
  );
  window.chatSocket = chatSocket;

  document.dispatchEvent(new Event("websocketReady"));
	console.log("websocketReady event fired")
}

function checkWebSocketAlive() {
  if (!window.chatSocket || window.chatSocket.readyState !== WebSocket.OPEN) {
    console.log("WebSocket not connected, attempting to reconnect...");
    createWebSocket();
  }
}

// *********************************************** //
document.addEventListener("DOMContentLoaded", () => {
  setInterval(checkWebSocketAlive, 1000);
  const chatContainer = document.getElementById("chat-container");
  if (!chatContainer) return; // Exit if chat container not found

  // Retrieve Django-passed variables from data attributes
  const roomName = chatContainer.dataset.roomName;
  const username = chatContainer.dataset.username;

  const messagesDiv = document.getElementById("messages");
  if (messagesDiv) {
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }
  const messageInput = document.getElementById("message-input");
  const sendButton = document.getElementById("send-button");

  if (!roomName || !username) {
    console.warn("Missing roomName or username data attributes.");
    return;
  }
  // Helper function to append messages to chat window
  function appendMessage(sender, message, isSentByCurrentUser) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");
    messageDiv.classList.add(isSentByCurrentUser ? "sent" : "received");
    messageDiv.innerHTML = `<strong>${sender}:</strong> <p>${message}</p>`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to bottom
  }

  // Send message on button click
  if (sendButton) {
    sendButton.addEventListener("click", (event) => {
      event.preventDefault();
      const message = messageInput.value.trim();
      if (!message) return;

      // Append message immediately for instant feedback
      appendMessage(username, message, true);

      // Send message to server
      chatSocket.send(JSON.stringify({ message, sender: username }));

      messageInput.value = "";
    });
  }

  // Send message on Enter key press
  if (messageInput) {
    messageInput.addEventListener("keyup", (event) => {
      if (event.key === "Enter") {
        sendButton.click();
      }
    });
  }

  function formatFileSize(bytes) {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  }

  function updateFileMessage(data, userIsSender) {
    const messageDiv = document.querySelector(
      `[data-temp-id="${data.tempId}"]`,
    );

    if (messageDiv) {
      const smallElement = messageDiv.querySelector("small");
      if (smallElement) {
        smallElement.textContent = "Upload complete";
        if (userIsSender) {
          return;
        }
      }

      // Update the file link if needed
      if (data.file_url) {
        const isImage = data.mime_type && data.mime_type.startsWith("image/");
        const fileElement = messageDiv.querySelector(".message-file");
        const imgElement = messageDiv.querySelector("img");
        // handle images
        if (isImage) {
          if (imgElement) {
            imgElement.src = data.file_url;
          } else {
            if (fileElement) {
              fileElement.innerHTML = `<img src="${data.file_url}" alt="${data.name}" style="max-width: 300px; max-height: 300px;">`;
            }
          }
        } else {
          // handle files
          if (fileElement) {
            fileElement.innerHTML = `<a href="${data.file_url}" download>Download ${data.name}</a>`;
          }

          if (imgElement) {
            imgElement.remove();
          }
        }
      }
    }
  }

  function displayFilePreview(data, isSentByCurrentUser) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");
    messageDiv.classList.add(isSentByCurrentUser ? "sent" : "received");
    messageDiv.dataset.tempId = data.tempId;

    let previewContent = "";
    if (data.mime_type && data.mime_type.startsWith("image/")) {
      previewContent = `
      <div class="message-file">
        <img 
          src="" 
          alt="Image preview loading..." 
          style="max-width: 300px; max-height: 300px;"
        />
        <div>Image file: ${data.name} (${formatFileSize(data.size)})</div>
      </div>
    `;
    } else {
      previewContent = `<div class="message-file">File: ${data.name} (${formatFileSize(data.size)})</div>`;
    }
    messageDiv.innerHTML = `
            <strong>${data.sender}:</strong>
            ${previewContent}
            <small>Waiting for Upload to complete</small>
        `;

    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }
  // ************************************************** //

  document.addEventListener("websocketReady", () => {
		console.log("websocket event received")
    // Get references to DOM elements

    chatSocket = window.chatSocket;

    // Handle incoming WebSocket messages
    chatSocket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "file_preview") {
        // Display file preview

        if (data.sender !== username) {
          displayFilePreview(data, false);
        }
      } else if (data.type === "file_uploaded") {
        const userIsSender = data.sender == username;

        // Update file message with permanent URL
        updateFileMessage(data, userIsSender);
      } else {
        // Regular text message
        const { message, sender } = data;
        if (sender !== username) {
          appendMessage(sender, message, false);
        }
      }
    };

    chatSocket.onclose = (event) => {
      console.error("Chat socket closed unexpectedly:", event);
    };

    chatSocket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  });
});
