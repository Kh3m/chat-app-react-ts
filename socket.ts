import { io } from "socket.io-client";

// "undefined" means the URL will be computed from the `window.location` object
const socket = io("http://localhost:4000", {
  autoConnect: false,
});

export { socket };
