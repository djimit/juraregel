import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: "#1a365d", light: "#2b6cb0" },
        accent: { DEFAULT: "#38a169", light: "#68d391" },
      },
    },
  },
  plugins: [],
};
export default config;
