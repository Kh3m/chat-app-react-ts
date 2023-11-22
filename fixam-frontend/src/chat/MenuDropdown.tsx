const MenuDropdown = () => {
  return (
    <div
      id="menuDropdown"
      className="absolute right-0 mt-2 w-48 bg-white border border-gray-300 rounded-md shadow-lg hidden"
    >
      <ul className="py-2 px-3">
        <li>
          <a
            href="#"
            className="block px-4 py-2 text-gray-800 hover:text-gray-400"
          >
            Option 1
          </a>
        </li>
        <li>
          <a
            href="#"
            className="block px-4 py-2 text-gray-800 hover:text-gray-400"
          >
            Option 2
          </a>
        </li>
        {/* <!-- Add more menu options here --> */}
      </ul>
    </div>
  );
};

export default MenuDropdown;
