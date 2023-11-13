import { type ReactNode } from "react";

interface Props {
  side: string;
  image: string | ReactNode;
}
const InputIcon = ({ image, side }: Props) => {
  const classeNames: { [key: string]: string } = {
    left: "bg-gradient-to-tr left-0 top-0 bottom-0 rounded-tl-lg rounded-bl-lg",
    right: "right-0 top-0 bottom-0 rounded-tr-lg rounded-br-lg",
  };
  return (
    <span
      className={`${classeNames[side]}
      inline-flex justify-center  from-pri-default to-pri-600 
    items-center absolute py-4 px-5`}
    >
      {typeof image === "string" ? (
        <img src={image} alt="Search" className="w-4 h-4" />
      ) : (
        image
      )}
    </span>
  );
};

export default InputIcon;
