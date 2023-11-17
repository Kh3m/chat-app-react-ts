import iconMenu from "../assets/icons/icon-menu.png";

interface Props {
  hideSideBar: boolean;
  handleSideBarVisibility: () => void;
}
const SideBarHeader = ({ hideSideBar, handleSideBarVisibility }: Props) => {
  return (
    <header className="p-4 border-b border-gray-300 flex justify-between items-center bg-pri-default text-white">
      {!hideSideBar && <h1 className="text-2xl font-semibold">Fixam Chat</h1>}
      <div className="relative">
        <button
          onClick={handleSideBarVisibility}
          id="menuButton"
          className="focus:outline-none"
        >
          {!hideSideBar && (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5 text-gray-100"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
              <path d="M2 10a2 2 0 012-2h12a2 2 0 012 2 2 2 0 01-2 2H4a2 2 0 01-2-2z" />
            </svg>
          )}
          {hideSideBar && <img src={iconMenu} alt="icon menu" />}
        </button>

        {/* <!-- Menu Dropdown --> */}
      </div>
    </header>
  );
};

export default SideBarHeader;
