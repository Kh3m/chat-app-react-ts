import ChatArea from "./ChatArea";
import SideBar from "./SideBar";
import { useState, useEffect } from "react";
import UsernameField from "./UsernameField";
import useWebSocket, { ReadyState } from "react-use-websocket";
import { MessageType } from "./ChatMessage";

const Chat = () => {
  const [hideSideBar, setHideSideBar] = useState(false);
  const [welcomeMessage, setWelcomeMessage] = useState("");
  const [conversationId, setConversationId] = useState("");
  const [messageHistory, setMessageHistory] = useState<any>([]);
  const [message, setMessage] = useState("");
  const [name, setName] = useState("");

  // const [username, setUsername] = useState("ws://localhost:8000/");
  const url = "wss://fixam-chat-app.onrender.com";

  const { readyState, sendJsonMessage } = useWebSocket(url, {
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
        case "conversation_created":
          // setWelcomeMessage(data.message);
          setConversationId(data.conversation_id);
          console.log(data);
          break;
        case "incoming_message":
          // setWelcomeMessage(data.message);
          console.log(data);
          break;
        case "chat_message_echo":
          setMessageHistory((prev: any) => prev.concat(data));
          break;
        case "chat_message_echo":
          setMessageHistory((prev: any) => prev.concat(data));
          break;
        default:
          console.log("Unknown message type!", data);
          break;
      }
    },
  });

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
    sendJsonMessage({
      type: "start_conversation",
      data: {
        email: "khem6333@gmail.com",
        username,
      },
    });
  };

  const handleSendMessage = (msg: MessageType) => {
    sendJsonMessage({
      ...msg,
      conversationId,
      fromUserEmail: "khem6333@gmail.com",
    });
    console.log({
      ...msg,
      conversationId,
      fromUserEmail: "khem6333@gmail.com",
    });
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
        <ChatArea
          hideSideBar={hideSideBar}
          handleSendMessage={handleSendMessage}
        />
      </div>
    </div>
  );
};

export default Chat;
