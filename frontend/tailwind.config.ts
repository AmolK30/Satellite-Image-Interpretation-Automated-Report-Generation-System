import type { Config } from 'tailwindcss'

export default {
  darkMode: ['class'],
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Space Grotesk"', 'ui-sans-serif', 'system-ui'],
      },
      boxShadow: {
        glow: '0 0 60px rgba(56, 189, 248, 0.2)',
      },
      colors: {
        panel: {
          50: '#f6fafc',
          100: '#eef6fa',
          200: '#dfeff5',
          300: '#bfe6ef',
          400: '#9ccfe0',
          500: '#6fb3c8',
          600: '#4e92a0',
          700: '#3a6b78',
          800: '#274952',
          900: '#12262a',
        },
        cyan: {
          50: '#f2f9fa',
          100: '#e6f3f6',
          200: '#cfe8ec',
          300: '#9fd2dd',
          400: '#6fbccf',
          500: '#3d99ad',
          600: '#2f7284',
          700: '#24545f',
          800: '#193a3f',
          900: '#0f2628',
        },
        emerald: {
          50: '#f3fbf7',
          100: '#e8f8ef',
          200: '#cff1dd',
          300: '#a7e6bf',
          400: '#6fcf95',
          500: '#3aab6f',
          600: '#2f8a55',
          700: '#21663f',
          800: '#15462b',
          900: '#0a2b18',
        },
      },
      backgroundImage: {
        'cosmic-grid': 'radial-gradient(circle at top left, rgba(59,130,246,0.18), transparent 35%), radial-gradient(circle at top right, rgba(16,185,129,0.12), transparent 25%), linear-gradient(135deg, #020617 0%, #0f172a 50%, #111827 100%)',
      },
    },
  },
  plugins: [],
} satisfies Config
