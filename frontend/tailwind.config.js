// tailwind.config.js
module.exports = {
  darkMode: ["class"],
  content: [
    "./src/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}"
  ],
  theme: { extend: {} },
  plugins: [require("tailwindcss-animate")],
}
