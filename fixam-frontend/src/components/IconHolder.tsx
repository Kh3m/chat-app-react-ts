import { type ImageType } from "../utils/types";

interface Props {
  image: ImageType;
}
const IconHolder = ({ image }: Props) => {
  return (
    <span className="inline-flex items-center justify-center ">
      <img {...image} />
    </span>
  );
};
export default IconHolder;
