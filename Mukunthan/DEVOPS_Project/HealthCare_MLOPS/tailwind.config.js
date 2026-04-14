/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "primary-fixed": "#dae2ff",
        "on-tertiary-container": "#ffc5be",
        "surface-container-high": "#e6e8ea",
        "outline": "#737685",
        "on-surface": "#191c1e",
        "surface": "#f7f9fb",
        "on-error-container": "#93000a",
        "on-error": "#ffffff",
        "on-primary-fixed-variant": "#0040a2",
        "error-container": "#ffdad6",
        "tertiary-container": "#b90012",
        "surface-container-highest": "#e0e3e5",
        "surface-container": "#eceef0",
        "surface-bright": "#f7f9fb",
        "secondary-fixed-dim": "#b9c7df",
        "primary": "#003d9b",
        "secondary-container": "#d5e3fc",
        "on-secondary-fixed": "#0d1c2e",
        "on-primary": "#ffffff",
        "background": "#f7f9fb",
        "on-tertiary-fixed": "#410002",
        "on-primary-container": "#c4d2ff",
        "inverse-primary": "#b2c5ff",
        "surface-dim": "#d8dadc",
        "secondary-fixed": "#d5e3fc",
        "outline-variant": "#c3c6d6",
        "inverse-on-surface": "#eff1f3",
        "surface-container-lowest": "#ffffff",
        "tertiary-fixed": "#ffdad6",
        "secondary": "#515f74",
        "on-secondary-container": "#57657a",
        "on-tertiary": "#ffffff",
        "on-surface-variant": "#434654",
        "on-secondary": "#ffffff",
        "on-tertiary-fixed-variant": "#93000b",
        "on-secondary-fixed-variant": "#3a485b",
        "primary-container": "#0052cc",
        "tertiary": "#8c000a",
        "tertiary-fixed-dim": "#ffb4ab",
        "on-primary-fixed": "#001848",
        "on-background": "#191c1e",
        "surface-variant": "#e0e3e5",
        "surface-container-low": "#f2f4f6",
        "primary-fixed-dim": "#b2c5ff",
        "inverse-surface": "#2d3133",
        "error": "#ba1a1a",
        "surface-tint": "#0c56d0"
      },
      borderRadius: {
        "DEFAULT": "0.125rem",
        "lg": "0.25rem",
        "xl": "0.5rem",
        "full": "0.75rem"
      },
      fontFamily: {
        "headline": ["Manrope", "sans-serif"],
        "body": ["Inter", "sans-serif"],
        "label": ["Inter", "sans-serif"]
      },
      animation: {
        aurora: "aurora 60s linear infinite",
      },
      keyframes: {
        aurora: {
          from: {
            backgroundPosition: "50% 50%, 50% 50%",
          },
          to: {
            backgroundPosition: "350% 50%, 350% 50%",
          },
        },
      },
    },
  },
  plugins: [],
}
