// frappeSocket.js
import { io } from "socket.io-client";

// Connect to Frappe's socket server (adjust port/domain as needed)
const socket = io("http://192.168.1.180:9000", {
  transports: ["websocket"],
  reconnection: true,
});

// Optional: Join a default room
socket.emit("join_room", "room-name");

// Listen to connection status (optional)
socket.on("connect", () => {
  console.log("Connected WebSocket server");
});

export default socket;
