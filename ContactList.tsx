import Contact, { ContactType } from "./Contact";

interface Props {
  contacts?: ContactType[];
  handleAdminJoined?: (userRoom: string) => void;
}
const ContactList = ({ contacts, handleAdminJoined }: Props) => {
  return (
    <div className="overflow-y-auto h-screen p-3 mb-9 pb-20">
      {contacts?.map((contact, i) => (
        <Contact
          handleAdminJoined={handleAdminJoined}
          key={i}
          username={contact.username}
          status={contact.status}
        />
      ))}
    </div>
  );
};

export default ContactList;
