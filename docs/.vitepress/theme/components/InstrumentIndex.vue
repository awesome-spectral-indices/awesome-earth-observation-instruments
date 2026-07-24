<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { withBase } from 'vitepress'
import instrumentData from '../../data/instruments.json'

type PresenceFilter = 'any' | 'yes' | 'no'
type DateFilterMode = 'exact' | 'range'

type InstrumentRecord = {
  id: string
  name: string
  acronym: string
  platform: string
  platforms: string[]
  platform_type: string
  type: string
  operator: string
  operators: string[]
  start_date: string
  status: string
  availability: string
  contributors: string[]
  references: string[]
  has_bands: boolean
  has_srf: boolean
  data_access_points: string[]
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
const advancedOpen = ref(false)
const selectedDataAccess = ref<string[]>([])
const filters = reactive({
  id: '',
  name: '',
  acronym: '',
  type: '',
  platformType: '',
  platform: '',
  operator: '',
  status: '',
  availability: '',
  contributor: '',
  reference: '',
  dateMode: 'exact' as DateFilterMode,
  exactDate: '',
  fromDate: '',
  toDate: '',
  bands: 'any' as PresenceFilter,
  srf: 'any' as PresenceFilter
})

const dataAccessOptions = [
  { key: 'ee', label: 'Google Earth Engine' },
  { key: 'planetary_computer', label: 'Planetary Computer' },
  { key: 'cdse', label: 'Copernicus Data Space' },
  { key: 'eopf', label: 'EOPF Sentinel Zarr Samples' }
]

const normalizedQuery = computed(() => query.value.trim().toLowerCase())
const instrumentTypeOptions = computed(() =>
  sortedUnique(instruments.map((instrument) => instrument.type))
)
const platformTypeOptions = computed(() =>
  sortedUnique(instruments.map((instrument) => instrument.platform_type))
)
const statusOptions = computed(() =>
  sortedUnique(instruments.map((instrument) => instrument.status))
)
const availabilityOptions = computed(() =>
  sortedUnique(instruments.map((instrument) => instrument.availability))
)

const advancedFilterCount = computed(() => {
  const textAndSelectFilters = [
    filters.id,
    filters.name,
    filters.acronym,
    filters.type,
    filters.platformType,
    filters.platform,
    filters.operator,
    filters.status,
    filters.availability,
    filters.contributor,
    filters.reference
  ].filter((value) => value.trim()).length

  const dateFilters = filters.dateMode === 'exact'
    ? Number(Boolean(filters.exactDate))
    : Number(Boolean(filters.fromDate)) + Number(Boolean(filters.toDate))
  const resourceFilters =
    Number(filters.bands !== 'any') + Number(filters.srf !== 'any')

  return (
    textAndSelectFilters +
    dateFilters +
    resourceFilters +
    selectedDataAccess.value.length
  )
})

const filteredInstruments = computed(() => {
  return instruments.filter((instrument) => {
    if (
      normalizedQuery.value &&
      !instrument.search_text.includes(normalizedQuery.value)
    ) {
      return false
    }

    if (!includesFilter(instrument.id, filters.id)) return false
    if (!includesFilter(instrument.name, filters.name)) return false
    if (!includesFilter(instrument.acronym, filters.acronym)) return false
    if (filters.type && instrument.type !== filters.type) return false
    if (
      filters.platformType &&
      instrument.platform_type !== filters.platformType
    ) {
      return false
    }
    if (!includesFilter(instrument.platforms.join(' '), filters.platform)) {
      return false
    }
    if (!includesFilter(instrument.operators.join(' '), filters.operator)) {
      return false
    }
    if (filters.status && instrument.status !== filters.status) return false
    if (
      filters.availability &&
      instrument.availability !== filters.availability
    ) {
      return false
    }
    if (
      !includesFilter(instrument.contributors.join(' '), filters.contributor)
    ) {
      return false
    }
    if (!includesFilter(instrument.references.join(' '), filters.reference)) {
      return false
    }
    if (!matchesDateFilter(instrument.start_date)) return false
    if (!matchesPresence(instrument.has_bands, filters.bands)) return false
    if (!matchesPresence(instrument.has_srf, filters.srf)) return false
    if (
      !selectedDataAccess.value.every((provider) =>
        instrument.data_access_points.includes(provider)
      )
    ) {
      return false
    }

    return true
  })
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

function sortedUnique(values: string[]) {
  return Array.from(new Set(values.filter(Boolean))).sort((left, right) =>
    left.localeCompare(right)
  )
}

function includesFilter(value: string, filter: string) {
  const normalizedFilter = filter.trim().toLowerCase()
  return !normalizedFilter || value.toLowerCase().includes(normalizedFilter)
}

function matchesDateFilter(startDate: string) {
  if (filters.dateMode === 'exact') {
    return !filters.exactDate || startDate === filters.exactDate
  }

  if (filters.fromDate && startDate < filters.fromDate) return false
  if (filters.toDate && startDate > filters.toDate) return false
  return true
}

function matchesPresence(value: boolean, filter: PresenceFilter) {
  if (filter === 'any') return true
  return filter === 'yes' ? value : !value
}

function clearAdvancedFilters() {
  filters.id = ''
  filters.name = ''
  filters.acronym = ''
  filters.type = ''
  filters.platformType = ''
  filters.platform = ''
  filters.operator = ''
  filters.status = ''
  filters.availability = ''
  filters.contributor = ''
  filters.reference = ''
  filters.dateMode = 'exact'
  filters.exactDate = ''
  filters.fromDate = ''
  filters.toDate = ''
  filters.bands = 'any'
  filters.srf = 'any'
  selectedDataAccess.value = []
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
      <div class="search-actions">
        <button
          v-if="query"
          class="clear-button"
          type="button"
          @click="query = ''"
        >
          Clear
        </button>
        <button
          class="advanced-toggle"
          :class="{ 'is-open': advancedOpen }"
          type="button"
          aria-controls="advanced-instrument-search"
          :aria-expanded="advancedOpen"
          @click="advancedOpen = !advancedOpen"
        >
          <span>{{ advancedOpen ? 'Hide advanced search' : 'Advanced search' }}</span>
          <span v-if="advancedFilterCount" class="filter-count">
            {{ advancedFilterCount }}
          </span>
        </button>
      </div>
    </div>

    <Transition name="advanced-panel">
      <section
        v-if="advancedOpen"
        id="advanced-instrument-search"
        class="advanced-search"
        aria-label="Advanced instrument search"
      >
        <header class="advanced-header">
          <div>
            <span class="advanced-eyebrow">Structured filters</span>
            <h2>Advanced search</h2>
            <p>
              Combine metadata, temporal, spectral, and data-access filters.
            </p>
          </div>
          <button
            v-if="advancedFilterCount"
            class="reset-button"
            type="button"
            @click="clearAdvancedFilters"
          >
            Reset {{ advancedFilterCount }} filters
          </button>
        </header>

        <div class="filter-section">
          <h3>Instrument metadata</h3>
          <div class="filter-grid">
            <label class="filter-field">
              <span>Instrument ID</span>
              <input
                v-model="filters.id"
                class="filter-input"
                type="search"
                placeholder="e.g. MSI_S2A"
              >
            </label>
            <label class="filter-field">
              <span>Name</span>
              <input
                v-model="filters.name"
                class="filter-input"
                type="search"
                placeholder="Name contains..."
              >
            </label>
            <label class="filter-field">
              <span>Acronym</span>
              <input
                v-model="filters.acronym"
                class="filter-input"
                type="search"
                placeholder="e.g. OLCI"
              >
            </label>
            <label class="filter-field">
              <span>Instrument type</span>
              <select v-model="filters.type" class="filter-input">
                <option value="">Any type</option>
                <option
                  v-for="value in instrumentTypeOptions"
                  :key="value"
                  :value="value"
                >
                  {{ headingText(value) }}
                </option>
              </select>
            </label>
            <label class="filter-field">
              <span>Platform type</span>
              <select v-model="filters.platformType" class="filter-input">
                <option value="">Any platform type</option>
                <option
                  v-for="value in platformTypeOptions"
                  :key="value"
                  :value="value"
                >
                  {{ headingText(value) }}
                </option>
              </select>
            </label>
            <label class="filter-field">
              <span>Platform</span>
              <input
                v-model="filters.platform"
                class="filter-input"
                type="search"
                placeholder="e.g. Sentinel-3"
              >
            </label>
            <label class="filter-field">
              <span>Operator</span>
              <input
                v-model="filters.operator"
                class="filter-input"
                type="search"
                placeholder="e.g. ESA"
              >
            </label>
            <label class="filter-field">
              <span>Status</span>
              <select v-model="filters.status" class="filter-input">
                <option value="">Any status</option>
                <option
                  v-for="value in statusOptions"
                  :key="value"
                  :value="value"
                >
                  {{ headingText(value) }}
                </option>
              </select>
            </label>
            <label class="filter-field">
              <span>Availability</span>
              <select v-model="filters.availability" class="filter-input">
                <option value="">Any availability</option>
                <option
                  v-for="value in availabilityOptions"
                  :key="value"
                  :value="value"
                >
                  {{ headingText(value) }}
                </option>
              </select>
            </label>
            <label class="filter-field">
              <span>Contributor</span>
              <input
                v-model="filters.contributor"
                class="filter-input"
                type="search"
                placeholder="GitHub username or URL"
              >
            </label>
            <label class="filter-field filter-field-wide">
              <span>Reference URL</span>
              <input
                v-model="filters.reference"
                class="filter-input"
                type="search"
                placeholder="DOI, domain, or URL contains..."
              >
            </label>
          </div>
        </div>

        <div class="filter-section">
          <h3>Start date</h3>
          <div class="date-controls">
            <label class="filter-field">
              <span>Date filter</span>
              <select v-model="filters.dateMode" class="filter-input">
                <option value="exact">Exact date</option>
                <option value="range">Date range</option>
              </select>
            </label>
            <label v-if="filters.dateMode === 'exact'" class="filter-field">
              <span>Started on</span>
              <input
                v-model="filters.exactDate"
                class="filter-input"
                type="date"
              >
            </label>
            <template v-else>
              <label class="filter-field">
                <span>From</span>
                <input
                  v-model="filters.fromDate"
                  class="filter-input"
                  type="date"
                >
              </label>
              <label class="filter-field">
                <span>To</span>
                <input
                  v-model="filters.toDate"
                  class="filter-input"
                  type="date"
                >
              </label>
            </template>
          </div>
        </div>

        <div class="filter-section resource-section">
          <div>
            <h3>Spectral resources</h3>
            <div class="resource-grid">
              <label class="filter-field">
                <span>Band definitions</span>
                <select v-model="filters.bands" class="filter-input">
                  <option value="any">Any</option>
                  <option value="yes">Available</option>
                  <option value="no">Not available</option>
                </select>
              </label>
              <label class="filter-field">
                <span>Spectral response function</span>
                <select v-model="filters.srf" class="filter-input">
                  <option value="any">Any</option>
                  <option value="yes">Available</option>
                  <option value="no">Not available</option>
                </select>
              </label>
            </div>
          </div>

          <fieldset class="provider-fieldset">
            <legend>Data access</legend>
            <p>Selected providers must all be available.</p>
            <div class="provider-grid">
              <label
                v-for="provider in dataAccessOptions"
                :key="provider.key"
                class="provider-option"
              >
                <input
                  v-model="selectedDataAccess"
                  type="checkbox"
                  :value="provider.key"
                >
                <span>{{ provider.label }}</span>
              </label>
            </div>
          </fieldset>
        </div>
      </section>
    </Transition>

    <p class="search-count">
      Showing {{ filteredInstruments.length }} of {{ instruments.length }} instruments.
      <span v-if="advancedFilterCount">
        {{ advancedFilterCount }} advanced
        {{ advancedFilterCount === 1 ? 'filter' : 'filters' }} applied.
      </span>
    </p>

    <p v-if="!filteredInstruments.length" class="empty-state">
      No instruments match the current search and filters.
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
  align-items: stretch;
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

.search-actions {
  display: flex;
  flex: none;
  gap: 0.6rem;
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

.advanced-toggle {
  display: inline-flex;
  gap: 0.55rem;
  align-items: center;
  justify-content: center;
  min-width: 10.5rem;
  border: 1px solid color-mix(in srgb, var(--vp-c-brand-1) 45%, var(--vp-c-divider));
  border-radius: 999px;
  padding: 0 1rem;
  background:
    linear-gradient(
      135deg,
      color-mix(in srgb, var(--vp-c-brand-1) 16%, transparent),
      color-mix(in srgb, var(--vp-c-brand-2) 7%, transparent)
    ),
    var(--vp-c-bg);
  color: var(--vp-c-text-1);
  cursor: pointer;
  font-weight: 750;
}

.advanced-toggle:hover,
.advanced-toggle.is-open {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}

.filter-count {
  display: inline-grid;
  min-width: 1.45rem;
  min-height: 1.45rem;
  place-items: center;
  border-radius: 999px;
  background: var(--vp-c-brand-1);
  color: var(--vp-c-bg);
  font-size: 0.75rem;
  line-height: 1;
}

.advanced-search {
  position: relative;
  overflow: hidden;
  margin-top: 1rem;
  border: 1px solid color-mix(in srgb, var(--vp-c-brand-1) 30%, var(--vp-c-divider));
  border-radius: 24px;
  padding: 1.25rem;
  background:
    radial-gradient(
      circle at top right,
      color-mix(in srgb, var(--vp-c-brand-1) 13%, transparent),
      transparent 34%
    ),
    var(--vp-c-bg-soft);
}

.advanced-header {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  justify-content: space-between;
}

.advanced-header h2 {
  margin: 0.15rem 0 0;
  border: 0;
  padding: 0;
  font-size: 1.35rem;
}

.advanced-header p,
.provider-fieldset p {
  margin: 0.3rem 0 0;
  color: var(--vp-c-text-2);
  font-size: 0.88rem;
}

.advanced-eyebrow {
  color: var(--vp-c-brand-1);
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.13em;
  text-transform: uppercase;
}

.reset-button {
  flex: none;
  border: 0;
  padding: 0.35rem 0;
  background: transparent;
  color: var(--vp-c-brand-1);
  cursor: pointer;
  font-weight: 750;
}

.reset-button:hover {
  text-decoration: underline;
}

.filter-section {
  margin-top: 1.15rem;
  border-top: 1px solid var(--vp-c-divider);
  padding-top: 1rem;
}

.filter-section h3,
.provider-fieldset legend {
  margin: 0 0 0.75rem;
  color: var(--vp-c-text-1);
  font-size: 0.9rem;
  font-weight: 800;
  letter-spacing: 0.02em;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.8rem;
}

.filter-field {
  display: grid;
  gap: 0.35rem;
  color: var(--vp-c-text-2);
  font-size: 0.78rem;
  font-weight: 700;
}

.filter-field-wide {
  grid-column: span 2;
}

.filter-input {
  width: 100%;
  min-height: 2.55rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 0.55rem 0.7rem;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font: inherit;
  font-size: 0.88rem;
  font-weight: 500;
}

.filter-input:focus {
  border-color: var(--vp-c-brand-1);
  outline: 2px solid color-mix(in srgb, var(--vp-c-brand-1) 25%, transparent);
}

.date-controls {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.8rem;
}

.resource-section {
  display: grid;
  grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
  gap: 1.5rem;
}

.resource-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.8rem;
}

.provider-fieldset {
  min-width: 0;
  margin: 0;
  border: 0;
  padding: 0;
}

.provider-fieldset legend {
  padding: 0;
}

.provider-fieldset p {
  margin: -0.55rem 0 0.75rem;
}

.provider-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.55rem;
}

.provider-option {
  display: flex;
  gap: 0.55rem;
  align-items: center;
  min-width: 0;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 0.65rem 0.75rem;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 650;
}

.provider-option:has(input:checked) {
  border-color: var(--vp-c-brand-1);
  background: color-mix(in srgb, var(--vp-c-brand-1) 12%, var(--vp-c-bg));
}

.provider-option input {
  flex: none;
  accent-color: var(--vp-c-brand-1);
}

.advanced-panel-enter-active,
.advanced-panel-leave-active {
  transition: opacity 180ms ease, transform 180ms ease;
}

.advanced-panel-enter-from,
.advanced-panel-leave-to {
  opacity: 0;
  transform: translateY(-6px);
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

  .search-actions,
  .clear-button,
  .advanced-toggle {
    width: 100%;
  }

  .clear-button,
  .advanced-toggle {
    min-height: 2.75rem;
  }

  .advanced-header {
    flex-direction: column;
  }

  .filter-grid,
  .date-controls,
  .resource-section,
  .resource-grid,
  .provider-grid {
    grid-template-columns: 1fr;
  }

  .filter-field-wide {
    grid-column: auto;
  }
}
</style>
