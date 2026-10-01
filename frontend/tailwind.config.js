/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../django_daisy_theme/templates/**/*.html",
    "../django_daisy_theme/templatetags/**/*.py",
    "../django_daisy_theme/static/**/*.js",
  ],
  theme: {
    extend: {
      fontFamily: {
        vazir: ["Vazirmatn", "system-ui", "-apple-system", "sans-serif"],
        inter: ["Inter", "system-ui", "-apple-system", "sans-serif"],
      },
    },
  },
  safelist: [
    {
      pattern: /(btn|badge|alert)-(primary|secondary|accent|info|success|warning|error|ghost|neutral)/,
    },
    {
      pattern: /table-(zebra|pin-rows|pin-cols)/,
    },
    {
      pattern: /drawer-(open|toggle|side|content)/,
    },
  ],
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      "light",
      "dark",
      "cupcake",
      "bumblebee",
      "emerald",
      "corporate",
      "synthwave",
      "retro",
      "cyberpunk",
      "valentine",
      "halloween",
      "garden",
      "forest",
      "aqua",
      "lofi",
      "pastel",
      "fantasy",
      "wireframe",
      "black",
      "luxury",
      "dracula",
      "cmyk",
      "autumn",
      "business",
      "acid",
      "lemonade",
      "night",
      "coffee",
      "winter",
      "dim",
      "nord",
      "sunset",
    ],
    darkTheme: "dark",
    base: true,
    styled: true,
    utils: true,
    rtl: true,
  },
};
