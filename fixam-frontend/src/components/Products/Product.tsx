import { ImageType } from "../../utils/types";
import IconHolder from "../IconHolder";

import wishList from "../../assets/wish-list-yes.png";
import { formatPrice } from "../../utils/number-formatter";
import Button from "../Button";

export type ProductType = {
  image: ImageType;
  status: "For Sale" | "Sold" | "New";
  favorite: boolean;
  title: string;
  price: number;
};

interface Props {
  product: ProductType;
}
const Product = ({
  product: { status, title, favorite, price, image },
}: Props) => {
  return (
    <article className="my-10">
      <div className="relative">
        <img {...image} className="object-cover" />
        <span
          className="py-2 px-4 absolute top-10 text-sm
        bg-pri-default text-white rounded-e-full"
        >
          {status}
        </span>
        <span className="absolute -bottom-7 right-7 cursor-pointer">
          <IconHolder
            image={{
              src: wishList,
              alt: favorite ? "Remove from wishlist" : "Add to wishlist",
            }}
          />
        </span>
      </div>
      <div className="p-5 bg-white  rounded-b-lg">
        <p className="text-black font-semibold my-2">{title}</p>
        <p className="text-pri-default font-semibold my-2">
          {formatPrice(price)}
        </p>
        <Button>Buy Now</Button>
      </div>
    </article>
  );
};

export default Product;
