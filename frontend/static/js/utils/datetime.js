export function formatDate(postTime) {
  const createdAt = new Date(postTime);
  const now = new Date();

  const diffMs = now.getTime() - createdAt.getTime(); // or: const diffMs = now - post created at;

  const seconds = Math.floor(diffMs / 1000) % 60;
  const minutes = Math.floor(diffMs / (1000 * 60)) % 60;
  const hours = Math.floor(diffMs / (1000 * 60 * 60)) % 24;
  const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (days === 0 && hours <= 24) {
    if (days === 0 && hours === 0 && minutes === 0) {
      return `${seconds} seconds ago`;
    } else if (days === 0 && hours === 0) {
      return `${minutes} minutes ago`;
    } else {
      return `${hours} hours ago`;
    }
  } else if (days > 0 && days <= 7) {
    return `${days} days ago`;
  } else {
    return `${createdAt.getDate()}/${createdAt.getMonth() + 1}/${createdAt.getFullYear()} ${createdAt.getHours()}:${createdAt.getMinutes()}`;
  }
}
