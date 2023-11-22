import { FieldValues, useForm } from "react-hook-form";

interface Props {
  handleUsername: (username: string) => void;
}

const UsernameField = ({ handleUsername }: Props) => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitSuccessful },
  } = useForm();
  const onSubmitForm = (data: FieldValues) => {
    handleUsername(data.username);
  };
  if (!isSubmitSuccessful)
    return (
      <form onSubmit={handleSubmit(onSubmitForm)}>
        <div className="text-red-200 text-md z-20">
          {errors.username?.type === "required" && "Please enter username"}
          {errors.username?.type === "minLength" &&
            "Username should be 3 or more chars"}
        </div>
        <div className="flex items-center z-30 p-20 fixed top-0 bottom-0 right-0 left-0 bg-slate-900">
          <input
            type="text"
            {...register("username", { required: true, minLength: 3 })}
            placeholder="Enter Username"
            className="flex-grow p-2 rounded-md border border-gray-400 focus:outline-none focus:border-blue-500"
          />
          <button className="bg-pri-default text-white px-4 py-2 rounded-md ml-2">
            Start Chat
          </button>
        </div>
      </form>
    );

  return null;
};

export default UsernameField;
