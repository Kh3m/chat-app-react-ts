import CustomMessage from "./CustomMessage";
import JoinMessage from "./JoinMessage";

// const messages: Message[] = [
//   { type: "incoming", message: "Hey, how's it going?" },
//   { type: "custom", message: "" },
//   { type: "join", message: "Shiphrah, join's the chat" },
//   {
//     type: "outgoing",
//     message: "Hi Abdul! I'm Shiphra, How may i help you today? ",
//   },
//   {
//     type: "outgoing",
//     message: "Thank you! ",
//   },
//   { type: "incoming", message: "", isTyping: true },
//   { type: "outgoing", message: "", isTyping: true },
// ];

export type MessageType = {
  type: "incoming" | "outgoing" | "custom" | "join";
  message: string;
  isTyping?: boolean;
};

interface Props {
  messages?: MessageType[];
  currentUser?: string;
}

const ChatMessage = ({ messages, currentUser }: Props) => {
  if (!currentUser) {
    console.log("Noooooooo", currentUser);
  }
  return (
    <div className="h-screen overflow-y-auto p-4 pb-36">
      {messages?.map(({ type, message, isTyping }, i) => {
        // if (type === "custom" && currentUser) return null;
        if (type === "custom")
          return <CustomMessage key={i} message={message} />;
        if (type === "join") return <JoinMessage key={i} message={message} />;
        return (
          <div
            key={i}
            className={`flex mb-4 cursor-pointer ${
              type === "incoming" ? "" : "justify-end"
            }`}
          >
            <div
              className={`w-9 h-9 rounded-full flex items-center justify-center  ${
                type === "incoming" ? "mr-2" : "ml-2 order-1"
              }`}
            >
              <img
                src={`${
                  type === "incoming"
                    ? "https://placehold.co/200x/ffa8e4/ffffff.svg?text=ʕ•́ᴥ•̀ʔ&font=Lato"
                    : "https://placehold.co/200x/fcb900/ffffff.svg?text=ʕ•́ᴥ•̀ʔ&font=Lato"
                }`}
                alt={`${type === "incoming" ? "User Avatar" : "My Avatar"} `}
                className="w-8 h-8 rounded-full"
              />
            </div>
            <div
              className={`flex max-w-96 rounded-lg p-3 gap-3 ${
                type === "incoming" ? "bg-white" : "bg-pri-600 "
              } `}
            >
              <p
                className={`${
                  type === "incoming" ? "text-gray-700" : "text-white"
                }`}
              >
                {isTyping ? <i>Typing...</i> : <span>{message}</span>}
              </p>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ChatMessage;
