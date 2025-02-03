// server.js

const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const cors = require("cors");

const app = express();
const server = http.createServer(app);
const io = socketIo(server);
io.set("origins", "*:*");

app.use(
  cors({
    origin: true,
  })
);

// Serve static files from the public directory
app.use(express.static(__dirname + "/public"));

io.on("connection", (socket) => {
  console.log("A user connected");

  // Listen for 'sendMessage' event from client
  socket.on("sendMessage", (data) => {
    console.log("Message received: ", data);
    // Broadcast the message to all other connected clients
    socket.broadcast.emit("receiveMessage", data);
  });

  socket.on("disconnect", () => {
    console.log("A user disconnected");
  });
});

server.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});
