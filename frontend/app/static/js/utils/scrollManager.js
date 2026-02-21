export const ScrollManager = (() => {
  const handlers = new Map();
  let ticking = false;

  function onScroll(e) {
    if (!ticking) {
      requestAnimationFrame(() => {
        handlers.forEach((handler) => handler(e));
        ticking = false;
      });
      ticking = true;
    }
  }

  window.addEventListener("scroll", onScroll, { passive: true });

  return {
    add(key, handler) {
      handlers.set(key, handler);
    },
    remove(key) {
      handlers.delete(key);
      window.removeEventListener("scroll", onScroll);
    },
    clear() {
      handlers.clear();
    },
  };
})();
