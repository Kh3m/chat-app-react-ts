import micTop from "../../assets/mic-top.png";
import micBottom from "../../assets/mic-bottom.png";

const Mic = () => {
  return (
    <div className="relative w-7 h-full">
      <img src={micTop} alt="Mic" className="absolute right-[18px]" />
      <img
        src={micBottom}
        alt="Mic"
        className="absolute left-0 right-0 bottom-0"
      />
    </div>
  );
};

export default Mic;
