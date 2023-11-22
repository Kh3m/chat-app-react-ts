export function ConnectionState({ isConnected }: { isConnected: boolean }) {
  return <p className=" capitalize text-red-600">State: {"" + isConnected}</p>;
}
