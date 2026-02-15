/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
      colors: {
        "tech-blue": "#00D4FF",
        "tech-purple": "#8B5CF6",
        "tech-dark": "#0A0E27",
        "tech-darker": "#050814",
      },
    },
  },
  plugins: [],
};
