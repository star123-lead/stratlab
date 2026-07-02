/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#0A0B0D',
        panel: '#16181C',
        line: '#2A2D33',
        paper: '#E8E6E1',
        amber: {
          DEFAULT: '#FF9F1C',
          dim: '#B8740F',
        },
        up: '#3DDC84',
        down: '#FF5C5C',
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      borderRadius: {
        sm: '3px',
        DEFAULT: '4px',
        md: '6px',
      },
    },
  },
  plugins: [],
}
