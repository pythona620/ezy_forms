export function getPreviousDate() {
  const today = new Date();
  today.setDate(today.getDate() - 1); // Set to previous day
  return today.toISOString().split("T")[0]; // Get the date part
}
