import { FaMicrophone, FaMicrophoneSlash } from "react-icons/fa6";
import InputIcon from "./InputIcon";
import searchSvg from "../../assets/search.svg";
import colors from "../../utils/colors";
import useMicrophone from "./useMicrophone";
import { type FormEvent, useRef } from "react";

const SearchInput = () => {
  const micRef = useRef<HTMLSpanElement>(null);
  const searchRef = useRef<HTMLInputElement>(null);
  const { isListening, searchText, setSearchText } = useMicrophone(
    micRef,
    searchRef
  );

  const onSubmit = (event: FormEvent) => {
    event.preventDefault();
    console.log(searchText);
  };

  return (
    <form onSubmit={onSubmit}>
      <div className="relative">
        <InputIcon image={searchSvg} side="left" />
        <input
          value={searchText}
          onChange={(event) => setSearchText(event.target.value)}
          ref={searchRef}
          placeholder="Search products, materials, and professionals"
          className="py-4 px-16 outline-0 rounded-lg md:w-[530px]"
        />
        <InputIcon
          image={
            !isListening ? (
              <span ref={micRef}>
                <FaMicrophone
                  cursor="pointer"
                  size="20px"
                  color={colors.primary}
                />
              </span>
            ) : (
              <FaMicrophoneSlash
                cursor="pointer"
                size="20px"
                color={colors.primary}
              />
            )
          }
          side="right"
        />
      </div>

      <div>{searchText}</div>
    </form>
  );
};

export default SearchInput;
