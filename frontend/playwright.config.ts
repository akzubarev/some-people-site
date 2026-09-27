import { defineConfig, devices } from '@playwright/test'
export default defineConfig({
  testDir: './tests', fullyParallel: true, retries: process.env.CI ? 1 : 0,
  reporter: [['list']], outputDir: 'test-results',
  use: { baseURL: process.env.E2E_BASE_URL || 'http://127.0.0.1:8080', trace: 'retain-on-failure' },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'], defaultBrowserType: 'chromium' } },
  ],
  webServer: process.env.E2E_BASE_URL ? undefined : {
    command: 'node node_modules/vite/bin/vite.js --host 0.0.0.0 --port 8080',
    port: 8080, reuseExistingServer: !process.env.CI,
  },
})
