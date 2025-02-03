// script.js

const socket = io("https://chatsglam.onrender.com");

const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const chatBox = document.getElementById("chatBox");
const backgroundInput = document.getElementById("backgroundInput");
const changeBackgroundButton = document.getElementById(
  "changeBackgroundButton"
);
const chatContainer = document.getElementById("chatContainer");

var gesture = "";

// Listen for incoming messages
socket.on("receiveMessage", (data) => {
  displayMessage(data.message, false);
});

// Send a message when the button is clicked
sendButton.addEventListener("click", () => {
  sendMessage();
});

// Send message on Enter key
messageInput.addEventListener("keypress", (event) => {
  if (event.key === "Enter") {
    sendMessage();
  }
});

function sendMessage() {
  const message = messageInput.value.trim();
  if (message) {
    displayMessage(message, true);
    socket.emit("sendMessage", { message });
    messageInput.value = "";
  }
}

function displayMessage(message, isSender) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("message");
  messageElement.textContent = message;
  messageElement.style.borderBottomLeftRadius = isSender ? "8px" : "0";
  messageElement.style.borderBottomRightRadius = isSender ? "0" : "8px";
  messageElement.style.textAlign = isSender ? "end" : "start";
  messageElement.style.float = isSender ? "right" : "left";
  messageElement.style.backgroundColor = "#075e54";
  messageElement.style.color = "#fff";
  messageElement.style.fontWeight = "bold";

  if (window.matchMedia("(max-width: 600px)").matches) {
    // If media query matches
    messageElement.style.marginRight = "15px";
  }

  chatBox.appendChild(messageElement);
  chatBox.scrollTop = chatBox.scrollHeight;

  const text = message.trim().toLowerCase();

  // Define the background images based on keywords
  const backgrounds = {
    happy: "url('./Images/happy.gif')",
    sad: "url('./Images/sad.gif')",
    angry: "url('./Images/angry.gif')",
    hi: "url('./Images/hi.gif')",
    hello: "url('./Images/hello.gif')",
    holiday: "url('./Images/holiday.gif')",
    play: "url('./Images/play.gif')",
    gaming: "url('./Images/gaming.gif')",
    party: "url('./Images/party.gif')",
    hbd: "url('./Images/hbd.gif')",
    anniversary: "url('./Images/anniversary.gif')",
    sick: "url('./Images/sick.gif')",
    congrats: "url('./Images/congrats.gif')",
    friends: "url('./Images/friends.gif')",
    thanks: "url('./Images/thanks.gif')",
    // Add more options as needed
  };

  if (text.includes("happy")) {
    if (
      text.includes("hbd") ||
      text.includes("birthday") ||
      text.includes("happybirthday")
    ) {
      gesture = "hbd";
    } else if (text.includes("anniversary") || text.includes("aniversary")) {
      gesture = "anniversary";
    } else {
      gesture = "happy";
    }
  } else if (text.includes("sad")) {
    gesture = "sad";
  } else if (text.includes("hello")) {
    gesture = "hello";
  } else if (text.includes("angry") || text.includes("anger")) {
    gesture = "angry";
  } else if (text.includes("hello")) {
    gesture = "hello";
  } else if (text.includes("hi")) {
    gesture = "hi";
  } else if (text.includes("holiday")) {
    gesture = "holiday";
  } else if (
    text.includes("hbd") ||
    text.includes("birthday") ||
    text.includes("happybirthday") ||
    text.includes("birthday")
  ) {
    gesture = "hbd";
  } else if (text.includes("play")) {
    gesture = "play";
  } else if (text.includes("friend")) {
    gesture = "friends";
  } else if (text.includes("sick") || text.includes("ill")) {
    gesture = "sick";
  } else if (text.includes("congrat")) {
    gesture = "congrats";
  } else if (text.includes("anniversary") || text.includes("aniversary")) {
    gesture = "anniversary";
  } else if (text.includes("party")) {
    gesture = "party";
  } else if (
    text.includes("game") ||
    text.includes("games") ||
    text.includes("gaming")
  ) {
    gesture = "gaming";
  } else if (text.includes("thanks") || text.includes("thankyou")) {
    gesture = "thanks";
  } else {
    gesture = "";
  }

  if (gesture != "") {
    if (window.matchMedia("(max-width: 600px)").matches) {
      // If media query matches
      document.getElementById("chatBox").style.width = "100%";
      document.getElementById("chatBox").style.backgroundImage =
        backgrounds[gesture];
      document.getElementById("chatBox").style.backgroundRepeat = "no-repeat";
      document.getElementById("chatBox").style.backgroundSize = "contain";
    } else {
      document.getElementById("chatBox").style.backgroundImage =
        backgrounds[gesture];
      document.getElementById("chatBox").style.backgroundRepeat = "no-repeat";
      document.getElementById("chatBox").style.backgroundSize = "cover";
    }
  } else {
    document.getElementById("chatBox").style.backgroundImage =
      "url('./Images/default.gif')";
  }
}
