const CustomMessage = ({ message }: { message: string }) => {
  return (
    <div className="text-center dark:text-white text-xs mb-4 px-24">
      <h4>
        Hi <span className="font-semibold">AbdulKareem</span>,
      </h4>
      <p className="text-pri-100">
        Thank you for reaching out to us! Your satisfaction is our priority, and
        we're here to help you. A friendly customer support representative will
        join this chat shortly to assist you.
      </p>

      <h4 className="text-left font-semibold my-4">
        While you wait, here are a couple of things to ensure a quick and
        efficient resolution:
      </h4>
      <ul className="text-left">
        <li className="p-2 bg-pri-100 text-pri-900 max-w-fit my-1 rounded-md cursor-pointer">
          If you have any order details, please have them handy.{" "}
        </li>
        <li className="p-2 bg-pri-100 text-pri-900 max-w-fit my-1 rounded-md cursor-pointer">
          Let us know how we can assist you today.
        </li>
      </ul>
    </div>
  );
};

export default CustomMessage;
