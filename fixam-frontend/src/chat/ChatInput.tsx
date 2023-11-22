import { MessageType } from "./ChatMessage";
import { FieldValues, useForm } from "react-hook-form";

interface Props {
  hideSideBar: boolean;
  handleSendMessage?: (msg: MessageType) => void;
}
const ChatInput = ({ hideSideBar, handleSendMessage }: Props) => {
  const {
    register,
    handleSubmit,
    formState: {},
  } = useForm();

  const submit = (data: FieldValues) => {
    if (handleSendMessage)
      handleSendMessage({
        type: "outgoing",
        isTyping: false,
        message: data.message,
      } as MessageType);
  };

  return (
    <footer
      className={`${
        !hideSideBar ? "w-3/4" : "w-[95%]"
      } transition-all duration-300 bg-white border-t border-gray-300 p-4 absolute bottom-0`}
    >
      <form onSubmit={handleSubmit(submit)}>
        <div className="flex items-center">
          <input
            {...register("message", { required: true })}
            type="text"
            placeholder="Type a message..."
            className="w-full p-2 rounded-md border border-gray-400 focus:outline-none focus:border-blue-500"
          />
          <button className="bg-pri-default text-white px-4 py-2 rounded-md ml-2">
            Send
          </button>
        </div>
      </form>
    </footer>
  );
};

export default ChatInput;
