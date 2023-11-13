import Icon from "./IconHolder";
import chevronRight from "../assets/chevron-right.svg";

const FeaturedBar = () => {
  return (
    <div className="py-4 px-6 bg-sec-600 text-white text-sm flex justify-between items-center">
      <span>Featured Products</span>
      <span className="flex items-center cursor-pointer">
        <span>View More</span> <Icon image={{ src: chevronRight, alt: "" }} />
      </span>
    </div>
  );
};

export default FeaturedBar;
