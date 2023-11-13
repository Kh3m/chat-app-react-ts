import { type ReactNode } from "react";

interface Props {
  variant?: string;
  color?: string;
  children: ReactNode;
}
const Button = ({ children, variant, color = "yellow" }: Props) => {
  const baseClass =
    "transition-color duration-500 rounded-lg text-white bg-pri-default";
  const outlinedType: { [key: string]: string } = {
    yellow:
      "py-2 px-6 rounded-lg border-2 border-pri-default bg-transparent hover:bg-pri-default",
    gray: "py-2 px-4 rounded-md border-2 border-gray-500 bg-transparent hover:bg-gray-500 text-pri-default",
  };
  switch (variant) {
    /**
     * w-icon : Button with icon
     */
    case "outlined":
      return (
        <button className={` ${baseClass} ${outlinedType[color]}`}>
          {children}
        </button>
      );
    case "w-icon":
      return (
        <button
          className={` ${baseClass} py-2 px-6
          flex space-x-2 justify-center items-center
          hover:bg-pri-600  `}
        >
          {children}
        </button>
      );
    default:
      return (
        <button className={` ${baseClass} py-2 px-6 hover:bg-pri-600`}>
          {children}
        </button>
      );
  }
};

export default Button;
