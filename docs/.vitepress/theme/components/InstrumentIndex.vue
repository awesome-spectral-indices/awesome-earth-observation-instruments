<script setup lang="ts">
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'
import instrumentData from '../../data/instruments.json'

type InstrumentRecord = {
  id: string
  name: string
  acronym: string
  platform: string
  platform_type: string
  type: string
  operator: string
  status: string
  availability: string
  href: string
  search_text: string
}

type InstrumentTypeGroup = {
  key: string
  label: string
  instruments: InstrumentRecord[]
}

type PlatformTypeGroup = {
  key: string
  label: string
  types: InstrumentTypeGroup[]
}

const instruments = instrumentData as InstrumentRecord[]
const query = ref('')

const normalizedQuery = computed(() => query.value.trim().toLowerCase())

const filteredInstruments = computed(() => {
  if (!normalizedQuery.value) return instruments

  return instruments.filter((instrument) =>
    instrument.search_text.includes(normalizedQuery.value)
  )
})

const groupedInstruments = computed<PlatformTypeGroup[]>(() => {
  const groups = new Map<string, Map<string, InstrumentRecord[]>>()

  for (const instrument of filteredInstruments.value) {
    if (!groups.has(instrument.platform_type)) {
      groups.set(instrument.platform_type, new Map())
    }

    const typeGroups = groups.get(instrument.platform_type)
    if (!typeGroups) continue

    if (!typeGroups.has(instrument.type)) {
      typeGroups.set(instrument.type, [])
    }

    typeGroups.get(instrument.type)?.push(instrument)
  }

  return Array.from(groups.entries())
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([platformType, typeGroups]) => ({
      key: platformType,
      label: headingText(platformType),
      types: Array.from(typeGroups.entries())
        .sort(([left], [right]) => left.localeCompare(right))
        .map(([instrumentType, instrumentsForType]) => ({
          key: instrumentType,
          label: headingText(instrumentType),
          instruments: instrumentsForType.sort((left, right) =>
            left.id.localeCompare(right.id)
          )
        }))
    }))
})

function headingText(value: string) {
  return value
    .replace(/[-_]+/g, ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

function valueClass(prefix: string, value: string) {
  const normalizedValue = value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')

  return `${prefix}-${normalizedValue || 'unknown'}`
}
</script>

<template>
  <div class="instrument-index">
    <label class="search-label" for="instrument-search">Search instruments</label>
    <div class="search-row">
      <input
        id="instrument-search"
        v-model="query"
        class="search-input"
        type="search"
        placeholder="Try Sentinel, hyperspectral, ESA, active..."
        autocomplete="off"
      >
      <button
        v-if="query"
        class="clear-button"
        type="button"
        @click="query = ''"
      >
        Clear
      </button>
    </div>

    <p class="search-count">
      Showing {{ filteredInstruments.length }} of {{ instruments.length }} instruments.
    </p>

    <p v-if="!filteredInstruments.length" class="empty-state">
      No instruments match this search.
    </p>

    <section
      v-for="platformGroup in groupedInstruments"
      :key="platformGroup.key"
      class="platform-group"
    >
      <h2>{{ platformGroup.label }}</h2>

      <section
        v-for="typeGroup in platformGroup.types"
        :key="typeGroup.key"
        class="type-group"
      >
        <h3>{{ typeGroup.label }}</h3>

        <ul class="instrument-list">
          <li
            v-for="instrument in typeGroup.instruments"
            :key="instrument.id"
            class="instrument-card"
          >
            <a class="instrument-link" :href="withBase(instrument.href)">
              <span class="instrument-id">{{ instrument.id }}</span>
              <span class="instrument-name">{{ instrument.name }}</span>
              <span class="instrument-platform">({{ instrument.platform }})</span>
            </a>

            <div class="instrument-meta">
              <span v-if="instrument.operator" class="meta-badge meta-operator">
                {{ instrument.operator }}
              </span>
              <span
                v-if="instrument.status"
                class="meta-badge"
                :class="valueClass('status', instrument.status)"
              >
                {{ instrument.status }}
              </span>
              <span
                v-if="instrument.availability"
                class="meta-badge"
                :class="valueClass('availability', instrument.availability)"
              >
                {{ instrument.availability }}
              </span>
            </div>
          </li>
        </ul>
      </section>
    </section>
  </div>
</template>

<style scoped>
.instrument-index {
  margin-top: 2rem;
}

.search-label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--vp-c-text-1);
  font-size: 0.95rem;
  font-weight: 700;
}

.search-row {
  display: flex;
  gap: 0.75rem;
}

.search-input {
  width: 100%;
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  padding: 0.8rem 1rem;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font-size: 1rem;
}

.search-input:focus {
  border-color: var(--vp-c-brand-1);
  outline: 2px solid color-mix(in srgb, var(--vp-c-brand-1) 30%, transparent);
}

.clear-button {
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  padding: 0 1rem;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  cursor: pointer;
  font-weight: 700;
}

.clear-button:hover {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}

.search-count,
.empty-state {
  margin-top: 0.75rem;
  color: var(--vp-c-text-2);
}

.platform-group {
  margin-top: 2.5rem;
}

.type-group {
  margin-top: 1.5rem;
}

.instrument-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 0.85rem;
  margin: 1rem 0 0;
  padding: 0;
  list-style: none;
}

.instrument-card {
  border: 1px solid var(--vp-c-divider);
  border-radius: 18px;
  padding: 1rem;
  background:
    linear-gradient(135deg, color-mix(in srgb, var(--vp-c-brand-1) 8%, transparent), transparent),
    var(--vp-c-bg-soft);
}

.instrument-link {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  align-items: baseline;
  color: var(--vp-c-text-1);
  font-weight: 700;
  text-decoration: none;
}

.instrument-link:hover .instrument-id,
.instrument-link:hover .instrument-name {
  color: var(--vp-c-brand-1);
}

.instrument-id {
  font-family: var(--vp-font-family-mono);
}

.instrument-platform {
  color: var(--vp-c-text-2);
  font-weight: 500;
}

.instrument-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 0.75rem;
}

.meta-badge {
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  padding: 0.15rem 0.5rem;
  color: var(--vp-c-text-2);
  font-size: 0.78rem;
}

.meta-operator {
  background: color-mix(in srgb, var(--vp-c-text-2) 8%, transparent);
}

.status-operational,
.status-active {
  border-color: color-mix(in srgb, #1a7f37 50%, transparent);
  background: color-mix(in srgb, #1a7f37 14%, transparent);
  color: #1a7f37;
}

.status-planned {
  border-color: color-mix(in srgb, #8250df 50%, transparent);
  background: color-mix(in srgb, #8250df 14%, transparent);
  color: #8250df;
}

.status-experimental {
  border-color: color-mix(in srgb, #9a6700 55%, transparent);
  background: color-mix(in srgb, #bf8700 16%, transparent);
  color: #9a6700;
}

.status-retired,
.status-legacy {
  border-color: color-mix(in srgb, #cf222e 50%, transparent);
  background: color-mix(in srgb, #cf222e 13%, transparent);
  color: #cf222e;
}

.availability-public {
  border-color: color-mix(in srgb, #0969da 50%, transparent);
  background: color-mix(in srgb, #0969da 13%, transparent);
  color: #0969da;
}

.availability-private {
  border-color: color-mix(in srgb, #9a6700 55%, transparent);
  background: color-mix(in srgb, #bf8700 16%, transparent);
  color: #9a6700;
}

:global(.dark) .status-operational,
:global(.dark) .status-active {
  color: #7ee787;
}

:global(.dark) .status-planned {
  color: #d2a8ff;
}

:global(.dark) .status-experimental,
:global(.dark) .availability-private {
  color: #f2cc60;
}

:global(.dark) .status-retired,
:global(.dark) .status-legacy {
  color: #ffa198;
}

:global(.dark) .availability-public {
  color: #79c0ff;
}

@media (max-width: 640px) {
  .search-row {
    flex-direction: column;
  }

  .clear-button {
    min-height: 2.75rem;
  }
}
</style>
