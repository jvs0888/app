/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./templates/**/*.html",
      "./static/js/*.js",
      "./static/modules/*.js",
  ],
  theme: {
    extend: {
        colors: {
            yellow: '#ff0'
        }
    },
  },
  plugins: [],
}

