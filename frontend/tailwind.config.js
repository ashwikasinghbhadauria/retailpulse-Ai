/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e6eaf0',
          100: '#c2c9d9',
          200: '#9fa9c2',
          300: '#7c89ab',
          400: '#596994',
          500: '#001F3F', // navy primary
          600: '#001739',
          700: '#001133',
          800: '#000c2d',
          900: '#000727',
        },
        surface: {
          DEFAULT: '#ffffff', // white background
          foreground: '#001F3F', // navy text
        },
        dark: {
          bg: '#0B0F19',
          card: '#111827',
          border: '#1F2937',
          hover: '#1E293B',
          text: '#F3F4F6',
          muted: '#9CA3AF'
        }
      },
        fontFamily: {
          sans: ['Roboto', 'system-ui', 'sans-serif'],
        }
    },
  },
  plugins: [],
}
