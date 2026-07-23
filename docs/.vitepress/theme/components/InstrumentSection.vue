<script setup lang="ts">
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'
import instrumentDetails from '../../data/instrument-details.json'

type Fact = {
  label: string
  value: string
  url?: string
  link_text?: string
}

type Band = {
  id: string
  center_wavelength: string
  bandwidth: string
  common_name: string
  gsd: string
  description: string
  snr: string
  search_text: string
}

type DataAccessProduct = {
  label: string
  docs: string
  collection: string
}

type DataAccessProvider = {
  key: string
  title: string
  stac_endpoint: string
  products: DataAccessProduct[]
}

type LinkRecord = {
  label?: string
  url?: string
  id?: string
  name?: string
  platform?: string
  href?: string
  reason?: string
}

type InstrumentDetails = {
  id: string
  summary: string
  quick_facts: Fact[]
  spectral_summary: Fact[]
  bands: Band[]
  imaging: Fact[]
  data_access: DataAccessProvider[]
  external_catalogues: LinkRecord[]
  related: LinkRecord[]
  data_links: LinkRecord[]
  references: LinkRecord[]
}

const props = defineProps<{
  instrumentId: string
  section: string
}>()

const details = instrumentDetails as Record<string, InstrumentDetails>
const bandQuery = ref('')

const instrument = computed(() => details[props.instrumentId])
const normalizedBandQuery = computed(() => bandQuery.value.trim().toLowerCase())

const filteredBands = computed(() => {
  const bands = instrument.value?.bands ?? []
  if (!normalizedBandQuery.value) return bands

  return bands.filter((band) => band.search_text.includes(normalizedBandQuery.value))
})

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
  <div v-if="instrument" class="instrument-section">
    <p v-if="section === 'summary'" class="summary-text">
      {{ instrument.summary }}
    </p>

    <div v-else-if="section === 'quick-facts'" class="fact-grid">
      <div
        v-for="fact in instrument.quick_facts"
        :key="fact.label"
        class="fact-card"
      >
        <span class="fact-label">{{ fact.label }}</span>
        <span
          class="fact-value"
          :class="[
            fact.label === 'Status' ? valueClass('status', fact.value) : '',
            fact.label === 'Availability' ? valueClass('availability', fact.value) : ''
          ]"
        >
          {{ fact.value }}
        </span>
      </div>
    </div>

    <div v-else-if="section === 'spectral-summary'" class="fact-grid">
      <div
        v-for="fact in instrument.spectral_summary"
        :key="fact.label"
        class="fact-card"
      >
        <span class="fact-label">{{ fact.label }}</span>
        <span class="fact-value">{{ fact.value }}</span>
        <a
          v-if="fact.url"
          class="fact-link"
          :href="fact.url"
          download
        >
          {{ fact.link_text || 'Download' }}
        </a>
      </div>
    </div>

    <div v-else-if="section === 'bands'" class="bands-section">
      <p v-if="!instrument.bands.length" class="empty-state">
        No spectral band information is available.
      </p>

      <details v-else class="bands-panel" open>
        <summary>
          Show band table
          <span>{{ filteredBands.length }} of {{ instrument.bands.length }} bands</span>
        </summary>

        <div class="band-search">
          <input
            v-model="bandQuery"
            type="search"
            placeholder="Filter by band, wavelength, common name, GSD..."
            autocomplete="off"
          >
        </div>

        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Band</th>
                <th>Center wavelength (nm)</th>
                <th>Bandwidth (nm)</th>
                <th>Common name</th>
                <th>GSD (m)</th>
                <th>SNR</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="band in filteredBands" :key="band.id">
                <td>{{ band.id }}</td>
                <td>{{ band.center_wavelength }}</td>
                <td>{{ band.bandwidth }}</td>
                <td>{{ band.common_name || '-' }}</td>
                <td>{{ band.gsd || '-' }}</td>
                <td>{{ band.snr || '-' }}</td>
                <td>{{ band.description || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <p v-if="!filteredBands.length" class="empty-state">
          No bands match this filter.
        </p>
      </details>
    </div>

    <div v-else-if="section === 'imaging'">
      <p v-if="!instrument.imaging.length" class="empty-state">
        No imaging-specific metadata is available for this instrument.
      </p>

      <div v-else class="fact-grid">
        <div
          v-for="fact in instrument.imaging"
          :key="fact.label"
          class="fact-card"
        >
          <span class="fact-label">{{ fact.label }}</span>
          <span class="fact-value">{{ fact.value }}</span>
        </div>
      </div>
    </div>

    <div v-else-if="section === 'data-access'" class="card-grid">
      <p v-if="!instrument.data_access.length" class="empty-state">
        No structured data access metadata is available.
      </p>

      <article
        v-for="provider in instrument.data_access"
        :key="provider.key"
        class="info-card"
      >
        <h3>{{ provider.title }}</h3>

        <p v-if="provider.stac_endpoint">
          <strong>STAC endpoint:</strong>
          <a :href="provider.stac_endpoint">{{ provider.stac_endpoint }}</a>
        </p>

        <div
          v-for="product in provider.products"
          :key="`${provider.key}-${product.label}-${product.collection}`"
          class="product-row"
        >
          <span class="product-label">{{ product.label }}</span>
          <code v-if="product.collection">{{ product.collection }}</code>
          <a v-if="product.docs" :href="product.docs">Documentation</a>
        </div>
      </article>
    </div>

    <div v-else-if="section === 'external-catalogues'" class="card-grid">
      <p v-if="!instrument.external_catalogues.length" class="empty-state">
        No external catalogue links are available.
      </p>

      <a
        v-for="link in instrument.external_catalogues"
        :key="link.label"
        class="info-card link-card"
        :href="link.url"
      >
        <span>{{ link.label }}</span>
        <small>{{ link.url }}</small>
      </a>
    </div>

    <div v-else-if="section === 'related'" class="card-grid">
      <p v-if="!instrument.related.length" class="empty-state">
        No closely related instruments were found in the catalogue.
      </p>

      <a
        v-for="related in instrument.related"
        :key="related.id"
        class="info-card link-card"
        :href="withBase(related.href || '')"
      >
        <span>{{ related.id }}: {{ related.name }}</span>
        <small>{{ related.platform }} · {{ related.reason }}</small>
      </a>
    </div>

    <div v-else-if="section === 'data-links'" class="source-grid">
      <div>
        <h3>Data links</h3>
        <p v-if="!instrument.data_links.length" class="empty-state">
          No data links are available.
        </p>
        <ul v-else>
          <li v-for="link in instrument.data_links" :key="link.url">
            <a :href="link.url">{{ link.url }}</a>
          </li>
        </ul>
      </div>
    </div>

    <div v-else-if="section === 'references'" class="source-grid">
      <div>
        <h3>References</h3>
        <p v-if="!instrument.references.length" class="empty-state">
          No references are available.
        </p>
        <ul v-else>
          <li v-for="link in instrument.references" :key="link.url">
            <a :href="link.url">{{ link.url }}</a>
          </li>
        </ul>
      </div>
    </div>

    <div v-else-if="section === 'sources'" class="source-grid">
      <div>
        <h3>Data links</h3>
        <p v-if="!instrument.data_links.length" class="empty-state">
          No data links are available.
        </p>
        <ul v-else>
          <li v-for="link in instrument.data_links" :key="link.url">
            <a :href="link.url">{{ link.url }}</a>
          </li>
        </ul>
      </div>

      <div>
        <h3>References</h3>
        <p v-if="!instrument.references.length" class="empty-state">
          No references are available.
        </p>
        <ul v-else>
          <li v-for="link in instrument.references" :key="link.url">
            <a :href="link.url">{{ link.url }}</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.instrument-section {
  margin-top: 1rem;
}

.summary-text {
  border-left: 4px solid var(--vp-c-brand-1);
  border-radius: 14px;
  padding: 1rem 1.2rem;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font-size: 1.05rem;
  line-height: 1.7;
}

.fact-grid,
.card-grid,
.source-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 0.85rem;
}

.fact-card,
.info-card {
  border: 1px solid var(--vp-c-divider);
  border-radius: 18px;
  padding: 1rem;
  background:
    linear-gradient(135deg, color-mix(in srgb, var(--vp-c-brand-1) 7%, transparent), transparent),
    var(--vp-c-bg-soft);
}

.fact-label {
  display: block;
  color: var(--vp-c-text-2);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.fact-value {
  display: inline-block;
  margin-top: 0.45rem;
  color: var(--vp-c-text-1);
  font-weight: 750;
}

.fact-link {
  display: block;
  margin-top: 0.45rem;
  font-size: 0.88rem;
  font-weight: 700;
}

.status-operational,
.status-active,
.status-planned,
.status-experimental,
.status-retired,
.status-legacy,
.availability-public,
.availability-private {
  border-radius: 999px;
  padding: 0.15rem 0.55rem;
}

.status-operational,
.status-active {
  background: color-mix(in srgb, #1a7f37 14%, transparent);
  color: #1a7f37;
}

.status-planned {
  background: color-mix(in srgb, #8250df 14%, transparent);
  color: #8250df;
}

.status-experimental,
.availability-private {
  background: color-mix(in srgb, #bf8700 16%, transparent);
  color: #9a6700;
}

.status-retired,
.status-legacy {
  background: color-mix(in srgb, #cf222e 13%, transparent);
  color: #cf222e;
}

.availability-public {
  background: color-mix(in srgb, #0969da 13%, transparent);
  color: #0969da;
}

.bands-panel {
  border: 1px solid var(--vp-c-divider);
  border-radius: 18px;
  padding: 0.85rem;
  background: var(--vp-c-bg-soft);
}

.bands-panel summary {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  cursor: pointer;
  color: var(--vp-c-text-1);
  font-weight: 750;
}

.bands-panel summary span {
  color: var(--vp-c-text-2);
  font-size: 0.9rem;
  font-weight: 600;
}

.band-search input {
  width: 100%;
  margin-top: 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  padding: 0.75rem 1rem;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
}

.table-wrapper {
  overflow-x: auto;
  margin-top: 1rem;
}

.table-wrapper table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.92rem;
}

.table-wrapper th,
.table-wrapper td {
  border-bottom: 1px solid var(--vp-c-divider);
  padding: 0.55rem 0.65rem;
  text-align: left;
  white-space: nowrap;
}

.table-wrapper th {
  color: var(--vp-c-text-1);
}

.empty-state {
  color: var(--vp-c-text-2);
}

.info-card {
  color: var(--vp-c-text-1);
  text-decoration: none;
}

.info-card h3 {
  margin: 0 0 0.75rem;
}

.product-row {
  display: grid;
  gap: 0.35rem;
  border-top: 1px solid var(--vp-c-divider);
  padding-top: 0.75rem;
  margin-top: 0.75rem;
}

.product-label {
  color: var(--vp-c-text-2);
  font-size: 0.82rem;
  font-weight: 750;
  text-transform: uppercase;
}

.link-card {
  display: grid;
  gap: 0.35rem;
}

.link-card span {
  font-weight: 750;
}

.link-card small {
  overflow-wrap: anywhere;
  color: var(--vp-c-text-2);
}

.source-grid ul {
  padding-left: 1.1rem;
}

.source-grid a,
.info-card a {
  overflow-wrap: anywhere;
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
</style>
