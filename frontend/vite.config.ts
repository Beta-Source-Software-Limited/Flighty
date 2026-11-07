import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// In Docker, backend is resolved by Compose DNS. For native macOS use localhost.
const apiTarget = process.env.VITE_API_PROXY_TARGET || 'http://backend:8000';
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    proxy: {
      '/api': { target: apiTarget, changeOrigin: true },
    },
  },
});
