import type { Config } from 'tailwindcss';

/** Configuração Tailwind partilhada (preset) para apps e packages do AOS */
const config: Config = {
  darkMode: ['class'],
  content: [
    '../../apps/**/src/**/*.{ts,tsx,mdx}',
    '../../packages/ui/src/**/*.{ts,tsx}',
    '../../plugins/*/frontend/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef4ff', 100: '#d9e5ff', 200: '#bcd2ff', 300: '#8eb4ff', 400: '#598bff',
          500: '#3363ff', 600: '#1b41f5', 700: '#142fe1', 800: '#1728b6', 900: '#19288f',
        },
      },
      fontFamily: { sans: ['Inter', 'ui-sans-serif', 'system-ui'] },
      borderRadius: { xl: '1rem', '2xl': '1.25rem' },
    },
  },
  plugins: [],
};

export default config;
