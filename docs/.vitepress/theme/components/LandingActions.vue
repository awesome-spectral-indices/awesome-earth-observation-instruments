<script setup lang="ts">
import { withBase } from 'vitepress'
</script>

<template>
  <nav class="landing-actions" aria-label="Catalogue actions">
    <div class="landing-action-group">
      <span class="landing-action-label">Explore the catalogue</span>
      <div class="landing-action-row">
        <a
          class="landing-action landing-action-primary"
          :href="withBase('/instruments/')"
          aria-label="Explore the catalogue in the Instrument Index"
        >
          Instrument Index
        </a>
        <a
          class="landing-action landing-action-secondary"
          href="https://awesome-spectral-indices.github.io/xeo/"
          aria-label="Explore the catalogue through the Python API"
        >
          Python API <span class="landing-action-symbol" aria-hidden="true">↗</span>
        </a>
      </div>
    </div>

    <div class="landing-action-group landing-action-download-group">
      <span class="landing-action-label">Download the catalogue</span>
      <a
        class="landing-action landing-action-download"
        href="https://raw.githubusercontent.com/awesome-spectral-indices/awesome-earth-observation-instruments/refs/heads/main/catalogue/catalogue.json"
        aria-label="Download the catalogue as JSON"
      >
        JSON <span class="landing-action-symbol" aria-hidden="true">↓</span>
      </a>
    </div>
  </nav>
</template>
