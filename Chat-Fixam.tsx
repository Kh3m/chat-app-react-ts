import ChatArea from "./ChatArea";
import SideBar from "./SideBar";
import { useState, useEffect } from "react";
import UsernameField from "./UsernameField";
import useWebSocket, { ReadyState } from "react-use-websocket";

const Chat = () => {
  const [hideSideBar, setHideSideBar] = useState(false);
  const [welcomeMessage, setWelcomeMessage] = useState("");
  const [messageHistory, setMessageHistory] = useState<any>([]);
  const [message, setMessage] = useState("");
  const [name, setName] = useState("");

  // const [username, setUsername] = useState("ws://localhost:8000/");
  const url = "ws://localhost:8000/khem";

  const { readyState, sendJsonMessage } = useWebSocket(
    `ws://localhost:8000/something`,
    {
      onOpen: () => {
        console.log("Connected!");
      },
      onClose: () => {
        console.log("Disconnected!");
      },
      // onMessage handler
      onMessage: (e) => {
        const data = JSON.parse(e.data);
        switch (data.type) {
          case "welcome_message":
            setWelcomeMessage(data.message);
            break;
          case "chat_message_echo":
            setMessageHistory((prev: any) => prev.concat(data));
            break;
          default:
            console.log("Unknown message type!");
            break;
        }
      },
    }
  );

  sendJsonMessage({ type: "any", Love: "To Code" });
  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  function handleChangeMessage(e: any) {
    setMessage(e.target.value);
  }

  function handleChangeName(e: any) {
    setName(e.target.value);
  }

  const handleSubmit = () => {
    sendJsonMessage({
      type: "chat_message",
      message,
      name,
    });
    setName("");
    setMessage("");
  };

  const handleSideBarVisibility = () => {
    setHideSideBar(!hideSideBar);
  };

  const handleUsername = (username: string) => {
    // setUsername(username);
  };

  useEffect(() => {}, []);

  return (
    <div>
      <UsernameField handleUsername={handleUsername} />
      <div className="flex h-screen overflow-hidden">
        <SideBar
          hideSideBar={hideSideBar}
          handleSideBarVisibility={handleSideBarVisibility}
        />
        <ChatArea hideSideBar={hideSideBar} />
      </div>
    </div>
  );
};

export default Chat;
