/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        obsidian: {
          950: '#110F17',
          900: '#181423',
          800: '#231D31',
          700: '#352D48',
        },
        navy: {
          950: '#110F17',
          900: '#181423',
          800: '#231D31',
          700: '#352D48',
        },
        charcoal: {
          950: '#121216',
          900: '#1A1A22',
          800: '#252530',
        },
        roseGold: {
          300: '#FDA4AF',
          400: '#FB7185',
          500: '#F43F5E',
          600: '#E11D48',
          700: '#BE123C',
        },
        electric: {
          400: '#FB7185',
          500: '#F43F5E',
          600: '#E11D48',
          700: '#BE123C',
        },
        amethyst: {
          300: '#D8B4FE',
          400: '#C084FC',
          500: '#A855F7',
          600: '#9333EA',
        },
        purpleAccent: {
          400: '#C084FC',
          500: '#A855F7',
          600: '#9333EA',
        },
        champagne: {
          300: '#FDE68A',
          400: '#FBBF24',
          500: '#F59E0B',
          600: '#D97706',
        },
        cyanAccent: {
          400: '#FBBF24',
          500: '#F59E0B',
        },
        emeraldAccent: {
          400: '#34D399',
          500: '#10B981',
        },
        amberAccent: {
          400: '#FBBF24',
          500: '#F59E0B',
        },
        roseAccent: {
          400: '#FB7185',
          500: '#F43F5E',
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      boxShadow: {
        'glow-rose': '0 0 25px -5px rgba(244, 63, 94, 0.4)',
        'glow-blue': '0 0 25px -5px rgba(244, 63, 94, 0.4)',
        'glow-purple': '0 0 25px -5px rgba(168, 85, 247, 0.4)',
        'glow-amber': '0 0 25px -5px rgba(245, 158, 11, 0.4)',
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-glow': 'pulseGlow 3s ease-in-out infinite',
        'fade-in': 'fadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
        'slide-up': 'slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1)',
        'spin-slow': 'spin 12s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        pulseGlow: {
          '0%, 100%': { opacity: '0.6', filter: 'drop-shadow(0 0 12px rgba(244, 63, 94, 0.4))' },
          '50%': { opacity: '1', filter: 'drop-shadow(0 0 24px rgba(168, 85, 247, 0.8))' },
        },
        fadeIn: {
          '0%': { opacity: '0', transform: 'scale(0.98)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    },
  },
  plugins: [],
};
