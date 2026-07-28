<script setup lang="ts">
defineProps<{
  instrumentId: string
}>()
</script>

<template>
  <div class="instrument-identity" aria-label="Instrument identifier">
    <span class="instrument-identity-label">Instrument ID</span>
    <code class="instrument-identity-value">{{ instrumentId }}</code>
  </div>
</template>
