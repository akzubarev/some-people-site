/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.vue"],
  theme: {
    extend: {
      container: {
        center: true
      },
      fontSize: {
        '3xl': '1.75rem',
        '8xl': '3.5rem'
      },
      colors: {
        gray: {
          400: '#8A9099',
          700: '#262C33',
          800: '#1D2126',
          900: '#13161A',
          1000: '#101114',
        },
        'accent': {
          // 'green': '#00994D',
          'green': '#0f6999',
          'emerald': '#003d8c',
          'blue': '#004799'
        }
      },
    }
  },
  plugins: []
}
