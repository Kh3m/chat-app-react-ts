import ChatHeader from "./ChatHeader";
import ChatInput from "./ChatInput";
import ChatMessage, { MessageType } from "./ChatMessage";

interface Props {
  hideSideBar: boolean;
  currentUser?: string;
  handleSendMessage: (msg: MessageType) => void;
  messages?: MessageType[];
}
const ChatArea = ({
  hideSideBar,
  currentUser,
  messages,
  handleSendMessage,
}: Props) => {
  return (
    <div className="flex-1">
      <ChatHeader user={currentUser} />
      <ChatMessage currentUser={currentUser} messages={messages} />
      <ChatInput
        hideSideBar={hideSideBar}
        handleSendMessage={handleSendMessage}
      />
    </div>
  );
};

export default ChatArea;
