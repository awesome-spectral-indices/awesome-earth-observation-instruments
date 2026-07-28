<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  instrumentId: string
}>()

const tabs = [
  { id: 'characteristics', label: 'Characteristics' },
  { id: 'operational-timeline', label: 'Timeline' },
  { id: 'spectral-comparison', label: 'Spectral Comparison' },
  { id: 'bands', label: 'Bands' },
  { id: 'data-access', label: 'Data Access' },
  { id: 'external-catalogues', label: 'External Catalogues' },
  { id: 'related-instruments', label: 'Related Instruments' },
  { id: 'references', label: 'References' }
] as const

const activeTab = ref<(typeof tabs)[number]['id']>('characteristics')
const tabButtons = ref<HTMLButtonElement[]>([])

function selectTab(tabId: (typeof tabs)[number]['id'], focus = false) {
  activeTab.value = tabId

  if (focus) {
    const index = tabs.findIndex((tab) => tab.id === tabId)
    tabButtons.value[index]?.focus()
  }
}

function handleKeydown(event: KeyboardEvent, index: number) {
  let nextIndex: number | null = null

  if (event.key === 'ArrowRight') nextIndex = (index + 1) % tabs.length
  if (event.key === 'ArrowLeft') nextIndex = (index - 1 + tabs.length) % tabs.length
  if (event.key === 'Home') nextIndex = 0
  if (event.key === 'End') nextIndex = tabs.length - 1

  if (nextIndex === null) return

  event.preventDefault()
  selectTab(tabs[nextIndex].id, true)
}
</script>

<template>
  <div class="instrument-tabs">
    <div class="tab-list" role="tablist" aria-label="Instrument information">
      <button
        v-for="(tab, index) in tabs"
        :id="`instrument-tab-${tab.id}`"
        :key="tab.id"
        :ref="(element) => { if (element) tabButtons[index] = element as HTMLButtonElement }"
        type="button"
        role="tab"
        :aria-controls="`instrument-panel-${tab.id}`"
        :aria-selected="activeTab === tab.id"
        :tabindex="activeTab === tab.id ? 0 : -1"
        @click="selectTab(tab.id)"
        @keydown="handleKeydown($event, index)"
      >
        {{ tab.label }}
      </button>
    </div>

    <section
      v-show="activeTab === 'characteristics'"
      id="instrument-panel-characteristics"
      role="tabpanel"
      aria-labelledby="instrument-tab-characteristics"
      tabindex="0"
    >
      <h2>Quick Facts</h2>
      <InstrumentSection :instrument-id="props.instrumentId" section="quick-facts" />

      <h2>Spectral Characteristics</h2>
      <InstrumentSection :instrument-id="props.instrumentId" section="spectral-summary" />

      <h2>Imaging</h2>
      <InstrumentSection :instrument-id="props.instrumentId" section="imaging" />
    </section>

    <section
      v-show="activeTab === 'operational-timeline'"
      id="instrument-panel-operational-timeline"
      role="tabpanel"
      aria-labelledby="instrument-tab-operational-timeline"
      tabindex="0"
    >
      <h2>Operational Timeline</h2>
      <InstrumentTimeline :instrument-id="props.instrumentId" />
    </section>

    <section
      v-show="activeTab === 'spectral-comparison'"
      id="instrument-panel-spectral-comparison"
      role="tabpanel"
      aria-labelledby="instrument-tab-spectral-comparison"
      tabindex="0"
    >
      <h2>Spectral Comparison</h2>
      <SpectralComparison :instrument-id="props.instrumentId" />
    </section>

    <section
      v-show="activeTab === 'bands'"
      id="instrument-panel-bands"
      role="tabpanel"
      aria-labelledby="instrument-tab-bands"
      tabindex="0"
    >
      <h2>Bands</h2>
      <InstrumentSection :instrument-id="props.instrumentId" section="bands" />
    </section>

    <section
      v-show="activeTab === 'data-access'"
      id="instrument-panel-data-access"
      role="tabpanel"
      aria-labelledby="instrument-tab-data-access"
      tabindex="0"
    >
      <h2>Data Access</h2>
      <InstrumentSection :instrument-id="props.instrumentId" section="data-access" />

      <h2>Data Links</h2>
      <InstrumentSection :instrument-id="props.instrumentId" section="data-links" />
    </section>

    <section
      v-show="activeTab === 'external-catalogues'"
      id="instrument-panel-external-catalogues"
      role="tabpanel"
      aria-labelledby="instrument-tab-external-catalogues"
      tabindex="0"
    >
      <h2>External Catalogues</h2>
      <InstrumentSection :instrument-id="props.instrumentId" section="external-catalogues" />
    </section>

    <section
      v-show="activeTab === 'related-instruments'"
      id="instrument-panel-related-instruments"
      role="tabpanel"
      aria-labelledby="instrument-tab-related-instruments"
      tabindex="0"
    >
      <h2>Related Instruments</h2>
      <InstrumentSection :instrument-id="props.instrumentId" section="related" />
    </section>

    <section
      v-show="activeTab === 'references'"
      id="instrument-panel-references"
      role="tabpanel"
      aria-labelledby="instrument-tab-references"
      tabindex="0"
    >
      <h2>Sources and References</h2>
      <InstrumentSection :instrument-id="props.instrumentId" section="references" />
    </section>
  </div>
</template>

<style scoped>
.instrument-tabs {
  margin-top: 1.75rem;
}

.tab-list {
  display: flex;
  gap: 0.35rem;
  overflow-x: auto;
  padding: 0.35rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 16px;
  background: var(--vp-c-bg-soft);
  scrollbar-width: thin;
}

.tab-list button {
  flex: 0 0 auto;
  padding: 0.65rem 0.9rem;
  border: 0;
  border-radius: 11px;
  background: transparent;
  color: var(--vp-c-text-2);
  font: inherit;
  font-size: 0.88rem;
  font-weight: 700;
  white-space: nowrap;
  cursor: pointer;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.tab-list button:hover {
  color: var(--vp-c-text-1);
  background: color-mix(in srgb, var(--vp-c-brand-1) 9%, transparent);
}

.tab-list button[aria-selected='true'] {
  color: var(--vp-c-brand-1);
  background: color-mix(in srgb, var(--vp-c-brand-1) 15%, var(--vp-c-bg));
}

.tab-list button:focus-visible,
[role='tabpanel']:focus-visible {
  outline: 2px solid var(--vp-c-brand-1);
  outline-offset: 2px;
}

[role='tabpanel'] {
  min-width: 0;
}

[role='tabpanel'] > h2:first-child {
  margin-top: 1.75rem;
}

@media (max-width: 640px) {
  .instrument-tabs {
    margin-top: 1.25rem;
  }

  .tab-list {
    margin-inline: -0.25rem;
  }
}
</style>
