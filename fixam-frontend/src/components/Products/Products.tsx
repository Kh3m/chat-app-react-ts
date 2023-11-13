import Grid from "../Grid";
import Product, { ProductType } from "./Product";

const products: ProductType[] = [
  {
    image: {
      src: "https://help.rangeme.com/hc/article_attachments/360006928633/what_makes_a_good_product_image.jpg",
      alt: "Camera",
    },
    title: "Amazing Camera",
    price: 34_557,
    favorite: true,
    status: "For Sale",
  },
];
const Products = () => {
  return (
    <Grid cols={4}>
      {Array.from([...products, ...products, ...products, ...products]).map(
        (prod, i) => (
          <Product key={i} product={prod} />
        )
      )}
    </Grid>
  );
};

export default Products;
