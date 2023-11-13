const IconPlus = ({ name = "" }: { name?: string }) => {
  const classNames: { [key: string]: string } = {
    "": "bg-white text-pri-default",
    cat: "bg-black text-white",
  };
  return (
    <span
      className={`
    ${classNames[name]}
    rounded-full h-3 w-3 inline-flex justify-center items-center `}
    >
      <span className="inline-block text-xs">+</span>
    </span>
  );
};

export default IconPlus;
