import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";

export default defineConfig({
  // site: "https://<your-domain>",  // set when deploying
  integrations: [mdx()],
});
