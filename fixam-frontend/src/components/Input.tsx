import emailIcon from "../assets/email-icon.svg";

const Input = () => {
  return (
    <div className="inline-block relative h-10">
      <input
        className="outline-0 px-10 rounded-md h-full text-gray-600"
        placeholder="Enter E-Mail Address"
      />
      <img
        src={emailIcon}
        alt="icon"
        className="h-4 w-4 absolute top-3 left-3"
      />
    </div>
  );
};

export default Input;
