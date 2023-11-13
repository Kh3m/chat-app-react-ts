/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
 
  theme: {
    extend: {
      colors: {
        'black': "#1F1F1F",
        'pri': {
          '50': '#fffeea',
          '100': '#fffac5',
          '200': '#fff685',
          '300': '#ffeb46',
          '400': '#ffdb1b',
          'default': '#fcb900',
          '600': '#e29000',
          '700': '#bb6602',
          '800': '#984e08',
          '900': '#7c400b',
          '950': '#482100',
      },
      'blue': '#4054B2',
      },
      fontFamily: {
        poppins: "'Poppins', sans-serif",
      },
    },
  },
  plugins: [],
}

