import { ReactNode } from "react";

interface Props {
  rounded?: boolean;
  children: ReactNode;
  color: string;
  styles?: string;
}
const Banner = ({ rounded, children, color, styles }: Props) => {
  const colors: { [key: string]: string } = {
    yellow: "bg-pri-default md:h-[317px] h-96",
    blue: "bg-blue md:h-[217px] h-80",
    black: "bg-black md:h-[217px] h-80",
  };
  return (
    <section
      className={`${rounded && "rounded-xl"} 
      ${styles}
      ${colors[color]}  
      flex justify-center items-center
      w-full
      `}
    >
      {children}
    </section>
  );
};

export default Banner;
