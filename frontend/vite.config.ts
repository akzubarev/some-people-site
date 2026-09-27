import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: { outDir: 'dist' },
  server: {
    allowedHosts: ['v1.app.some-people.localhost', 'host.docker.internal'],
    proxy: Object.fromEntries(['/api', '/media', '/staticfiles'].map(path => [
      path, { target: process.env.API_URL || 'http://localhost:8000', changeOrigin: false },
    ])),
  },
  test: { environment: 'jsdom', include: ['src/**/*.test.{ts,tsx}'] },
})
