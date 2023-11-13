import Banner from "./Banner";
import Button from "./Button";
import Input from "./Input";

const NewsLetter = () => {
  return (
    <Banner color="black" styles="flex flex-col my-5 text-center text-white">
      <div className="my-2">
        <p className="text-lg">
          Hello there, new to <span className="text-pri-default">Fixam?</span>
        </p>
        <p className="text-xs">
          Subscribe to our newsletter to get updates on our latest offers!
        </p>
      </div>
      <div>
        <Input />
        <div className="mx-2 inline-block"></div>
        <Button variant="outlined" color="gray">
          Male
        </Button>
        <div className="mx-2 inline-block"></div>
        <Button variant="outlined" color="gray">
          Female
        </Button>
      </div>
    </Banner>
  );
};

export default NewsLetter;
