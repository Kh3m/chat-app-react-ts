const ChatHeader = ({ user }: { user?: string }) => {
  return (
    <header className="bg-white p-4 text-gray-700">
      <h1 className="text-2xl font-semibold">{user}</h1>
    </header>
  );
};

export default ChatHeader;
