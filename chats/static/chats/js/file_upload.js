document.addEventListener("DOMContentLoaded", () => {
  document.addEventListener("websocketReady", function () {
		console.log("file uploads connected")
    const messagesDiv = document.getElementById("messages");
    const fileButton = document.getElementById("file-button");
    const fileInput = document.getElementById("file-input");
    const chatContainer = document.getElementById("chat-container");
    const roomName = chatContainer.dataset.roomName;
    const username = chatContainer.dataset.username;

    // Get the existing WebSocket connection from the global scope
    const chatSocket = window.chatSocket;

    fileButton.addEventListener("click", function () {
      console.log(chatSocket);

      fileInput.click();
    });

    fileInput.addEventListener("change", function () {
      if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        sendFileOverWebSocket(file);
      }
    });

    function sendFileOverWebSocket(file) {
      const reader = new FileReader();
      const tempId = Date.now().toString();

      reader.onload = function (event) {
        const fileData = {
          type: "file",
          name: file.name,
          size: file.size,
          mime_type: file.type,
          data: event.target.result.split(",")[1], // Remove data URL prefix
          sender: username,
          room_name: roomName,
          temp_id: tempId,
        };
        console.log(fileData);

        // Show preview immediately
        showFilePreview(file, username, true, tempId);

        // Send via WebSocket
        chatSocket.send(JSON.stringify(fileData));

        // Clear the file input
        fileInput.value = "";
      };

      reader.onerror = function (error) {
        console.error("Error reading file:", error);
      };

      // Read as Data URL (base64 encoded)
      reader.readAsDataURL(file);
    }

    function showFilePreview(file, sender, isSentByCurrentUser, tempId) {
      console.log("Uploading");
      console.log(tempId);

      const messageDiv = document.createElement("div");
      messageDiv.classList.add("message");
      messageDiv.classList.add(isSentByCurrentUser ? "sent" : "received");
      messageDiv.dataset.tempId = tempId;

      let previewContent = "";
      if (file.type.startsWith("image/")) {
        previewContent = `<img src="${URL.createObjectURL(file)}" alt="Preview" style="max-width: 300px; max-height: 300px;">`;
      } else {
        previewContent = `<div class="message-file">File: ${file.name} (${formatFileSize(file.size)})</div>`;
      }

      messageDiv.innerHTML = `
            <strong>${sender}:</strong>
            ${previewContent}
            <small>Uploading...</small>
        `;

      messagesDiv.appendChild(messageDiv);
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    function formatFileSize(bytes) {
      if (bytes === 0) return "0 Bytes";
      const k = 1024;
      const sizes = ["Bytes", "KB", "MB", "GB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
    }
  });
});
