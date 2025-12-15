import { resolve } from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        playground: resolve(__dirname, 'playground/index.html'),
        docs: resolve(__dirname, 'docs/index.html'),
        research: resolve(__dirname, 'research-and-safety/index.html'),
        impact: resolve(__dirname, 'impact/index.html'),
      },
    },
  },
  server: {
    open: true
  }
})
