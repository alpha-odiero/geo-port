import path from 'path';
import {defineConfig} from 'vite';

export default defineConfig(() => {
  return {
    build: {
      rollupOptions: {
        input: {
          main: path.resolve(__dirname, 'index.html'),
          about: path.resolve(__dirname, 'about.html'),
          services: path.resolve(__dirname, 'services.html'),
          fleet: path.resolve(__dirname, 'fleet.html'),
          warehouse: path.resolve(__dirname, 'warehouse.html'),
          tracking: path.resolve(__dirname, 'tracking.html'),
          projects: path.resolve(__dirname, 'projects.html'),
          gallery: path.resolve(__dirname, 'gallery.html'),
          careers: path.resolve(__dirname, 'careers.html'),
          blog: path.resolve(__dirname, 'blog.html'),
          faq: path.resolve(__dirname, 'faq.html'),
          contact: path.resolve(__dirname, 'contact.html'),
        },
      },
    },
    resolve: {
      alias: {
        '@': path.resolve(__dirname, '.'),
      },
    },
    server: {
      hmr: process.env.DISABLE_HMR !== 'true',
      watch: process.env.DISABLE_HMR === 'true' ? null : {},
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
        },
      },
    },
  };
});
