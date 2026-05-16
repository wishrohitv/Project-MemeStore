export function parseUrlParams() {
  const urlParams = new URLSearchParams(location.search);
  return Object.fromEntries(urlParams.entries());
}
