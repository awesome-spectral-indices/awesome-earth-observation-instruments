import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Awesome Earth Observation Instruments",
  description: "Awesome Earth Observation Instruments",
  base: '/aeoi/',
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Instrument Index', link: '/instruments/' },
      { text: 'Schema', link: '/schema' },
      { text: 'Events', link: '/events' },
      { text: 'Contributing', link: '/contributing' },
      { text: 'Changelog', link: '/changelog' },
      { text: 'How to cite', link: '/publications' },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments' }
    ],

    search: {
      provider: 'local'
    },

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026-present David Montero Loaiza'
    }

  }
})
