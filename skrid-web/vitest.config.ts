import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    // Your Vitest configuration here
    environment: 'jsdom',
    globals: true,
  },
});
