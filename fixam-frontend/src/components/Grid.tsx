import { PropsWithChildren } from "react";

interface Props {
  cols: number;
}
const Grid = ({ cols, children }: PropsWithChildren<Props>) => {
  const columns: { [key: number]: string } = {
    1: "grid-cols-1",
    2: "grid-cols-2",
    3: "md:grid-cols-3",
    4: "lg:grid-cols-4",
  };
  return <div className={`grid gap-5 ${columns[cols]}`}>{children}</div>;
};

export default Grid;
