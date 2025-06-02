document.addEventListener('DOMContentLoaded', () => {
  const elements = document.querySelectorAll('.animate-on-scroll');

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          // Element enters viewport: Add classes for visible state
          entry.target.classList.add('opacity-100', 'translate-y-0', 'scale-100');
          // Remove initial state classes if present
          entry.target.classList.remove('opacity-0', 'translate-y-10', 'scale-90');
        } else {
          // Element exits viewport: Revert to initial state
          entry.target.classList.remove('opacity-100', 'translate-y-0', 'scale-100');
          entry.target.classList.add('opacity-0', 'translate-y-10', 'scale-90');
        }
      });
    },
    {
      threshold: 1.0, // Trigger when 100% of the element is visible
      rootMargin: '0px', // Optional: Adjusts when the observer triggers
    }
  );

  elements.forEach((element) => {
    observer.observe(element);
  });
});
