import ChatArea from "./ChatArea";
import SideBar from "./SideBar";
import { useEffect, useState } from "react";

import { socket } from "./socket";
import UsernameField from "./UsernameField";
import { ContactType } from "./Contact";
import { MessageType } from "./ChatMessage";

const Chat = () => {
  const [hideSideBar, setHideSideBar] = useState(false);
  const [adminJoined, setAdminJoned] = useState(false);
  const [contacts, setContacts] = useState<ContactType[]>([]);
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [currentUser, setCurrentUser] = useState("");

  const handleSideBarVisibility = () => {
    setHideSideBar(!hideSideBar);
  };

  // CHAT
  // const [isConnected, setIsConnected] = useState(socket.connected);

  useEffect(() => {
    socket.connect();

    socket.on("connected_users", (data) => {
      console.log(data);
      setContacts([...data]);
    });

    // socket.on("received_message", ({}) => {});

    socket.on("admin_joined", (data) => {
      socket.emit("prev_msg_before_admin_joins", {
        room: "admin", // TODO: Specify specific admin
      });
      setAdminJoned(true);

      // Send an event to join the admin's room that just joined the chat

      setMessages((prevMsgs) => [...prevMsgs, data.message]);
    });

    socket.on("received_message", (data) => {
      setMessages((prevMsgs) => [...prevMsgs, data]);
    });

    socket.on("received_msg_before_admin_joins", ({ messages }) => {
      console.log("received_msg_before_admin_joins", messages);
      // TODO:
      // setMessages((prevMsgs) => [...prevMsgs, messages]);
    });

    // function onConnect() {
    //   setIsConnected(true);
    // }

    // function onDisconnect() {
    //   setIsConnected(false);
    // }

    // socket.on("connect", onConnect);
    // socket.on("disconnect", onDisconnect);

    return () => {
      // socket.off("connect");
      // socket.off("disconnect");
      socket.disconnect();
    };
  }, [socket]);

  const handleUsername = (username: string) => {
    if (username === "admin") {
      socket.emit("is_admin", { username });
    } else {
      setCurrentUser(username);
      socket.emit("user_joined", { username });
    }
  };

  const handleSendMessage = (message: MessageType) => {
    if (message) {
      if (messages.length <= 0) {
        setMessages((prevMsgs) => [
          ...prevMsgs,
          message,
          { type: "custom", message: "" },
        ]);
        socket.emit("message", { message, room: currentUser });
      } else {
        setMessages((prevMsgs) => [...prevMsgs, message]);
        socket.emit("message", { message, room: currentUser });
      }
    }
  };

  const handleAdminJoined = (userRoom: string) => {
    const message = {
      type: "join",
      message: "Shiphrah, join's the chat",
      isTyping: false,
    } as MessageType;
    setCurrentUser(userRoom);
    // setMessages((prevMsgs) => [...prevMsgs, message]);
    socket.emit("admin_has_joined", { message, room: userRoom });
  };
  return (
    <div>
      <UsernameField handleUsername={handleUsername} />
      <div className="flex h-screen overflow-hidden">
        <SideBar
          contacts={contacts}
          hideSideBar={hideSideBar}
          handleSideBarVisibility={handleSideBarVisibility}
          handleAdminJoined={handleAdminJoined}
        />
        <ChatArea
          currentUser={currentUser}
          messages={messages}
          hideSideBar={hideSideBar}
          handleSendMessage={handleSendMessage}
        />
      </div>
    </div>
  );
};

export default Chat;
