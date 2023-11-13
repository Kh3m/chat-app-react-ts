export function formatPrice(price: number) {
  return new Intl.NumberFormat("en-ng", {
    currency: "ngn",
    style: "currency",
  }).format(price);
}
