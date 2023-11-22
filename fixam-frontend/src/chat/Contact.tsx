import { useState } from "react";

export type ContactType = {
  status: "active" | "pending";
  username: string;
  handleAdminJoined?: (userRoom: string) => void;
};

const Contact = ({ status, username, handleAdminJoined }: ContactType) => {
  const [isActive, setIsActive] = useState(false);

  const handleContactClick = () => {
    if (handleAdminJoined) handleAdminJoined(username);
    setIsActive(true);
  };
  return (
    <div
      onClick={isActive ? undefined : handleContactClick}
      className="flex items-center mb-4 cursor-pointer hover:bg-gray-100 p-2 rounded-md"
    >
      <div className="w-12 h-12 bg-gray-300 rounded-full mr-3">
        <img
          src="https://placehold.co/200x/ffa8e4/ffffff.svg?text=ʕ•́ᴥ•̀ʔ&font=Lato"
          alt="User Avatar"
          className="w-12 h-12 rounded-full"
        />
      </div>
      <div className="flex-1">
        <h2 className={`text-lg font-semibold`}>{username}</h2>
        <p
          className={`font-semibold text-sm ${
            isActive ? "text-green-500" : "text-gray-500 italic"
          }`}
        >
          {isActive ? "active" : status}
        </p>
      </div>
    </div>
  );
};

export default Contact;
