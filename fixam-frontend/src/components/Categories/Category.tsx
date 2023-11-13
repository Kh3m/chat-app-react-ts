import IconPlus from "../IconPlus";

const Category = () => {
  return (
    <li className="flex justify-between my-6 mx-2 text-sm cursor-pointer items-center ">
      <span className=" text-black ">Category</span> <IconPlus name="cat" />
    </li>
  );
};

export default Category;
