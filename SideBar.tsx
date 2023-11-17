import { ContactType } from "./Contact";
import ContactList from "./ContactList";
import SideBarHeader from "./SideBarHeader";

interface Props {
  hideSideBar: boolean;
  handleSideBarVisibility: () => void;
  handleAdminJoined?: (userRoom: string) => void;
  contacts?: ContactType[];
}

const SideBar = ({
  hideSideBar,
  handleAdminJoined,
  handleSideBarVisibility,
  contacts,
}: Props) => {
  return (
    <div
      className={`duration-300 transition-all ${
        !hideSideBar ? "w-1/4" : "w-[5%]"
      } bg-white border-r border-gray-300`}
    >
      <SideBarHeader
        hideSideBar={hideSideBar}
        handleSideBarVisibility={handleSideBarVisibility}
      />
      {!hideSideBar && (
        <ContactList
          contacts={contacts}
          handleAdminJoined={handleAdminJoined}
        />
      )}
    </div>
  );
};

export default SideBar;
