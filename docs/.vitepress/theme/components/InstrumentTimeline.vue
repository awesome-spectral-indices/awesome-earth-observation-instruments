<script setup lang="ts">
import { computed, ref } from 'vue'
import instrumentDetails from '../../data/instrument-details.json'

type TimelineMetadata = {
  name: string
  acronym: string
  type: string
  status: string
  start_date: string
  end_date: string
}

type InstrumentDetails = {
  id: string
  timeline: TimelineMetadata
}

type ChartRow = TimelineMetadata & {
  id: string
  start: Date
  end: Date
  isCurrent: boolean
  isOngoing: boolean
}

const props = defineProps<{
  instrumentId: string
}>()

const details = instrumentDetails as Record<string, InstrumentDetails>
const defaultComparisons = ['MSI_S2A', 'OLI2_L9', 'MODIS_TERRA']
const fallbackComparison = 'EMIT'
const chartWidth = 1040
const labelWidth = 250
const chartRight = 28
const plotWidth = chartWidth - labelWidth - chartRight
const rowHeight = 62
const chartTop = 58
const chartBottom = 58

const now = new Date()
const today = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()))

const initialIds = [
  props.instrumentId,
  ...defaultComparisons.filter((id) => id !== props.instrumentId)
]

if (defaultComparisons.includes(props.instrumentId)) {
  initialIds.push(fallbackComparison)
}

const selectedIds = ref([...new Set(initialIds.filter((id) => details[id]))])
const pendingId = ref('')

const availableInstruments = computed(() =>
  Object.values(details)
    .filter((instrument) => !selectedIds.value.includes(instrument.id))
    .sort((left, right) => left.id.localeCompare(right.id))
)

const rows = computed<ChartRow[]>(() =>
  selectedIds.value.flatMap((id) => {
    const instrument = details[id]
    if (!instrument?.timeline.start_date) return []

    const start = parseDate(instrument.timeline.start_date)
    const isOngoing = !instrument.timeline.end_date
    const end = isOngoing ? today : parseDate(instrument.timeline.end_date)
    if (!start || !end) return []

    return [{
      id,
      ...instrument.timeline,
      start,
      end,
      isCurrent: id === props.instrumentId,
      isOngoing
    }]
  })
)

const dateRange = computed(() => {
  const timestamps = rows.value.flatMap((row) => [row.start.getTime(), row.end.getTime()])
  const minimum = Math.min(...timestamps)
  const maximum = Math.max(...timestamps)
  const span = Math.max(maximum - minimum, 24 * 60 * 60 * 1000)

  return {
    minimum,
    maximum,
    span
  }
})

const axisTicks = computed(() => {
  if (!rows.value.length) return []

  const firstYear = new Date(dateRange.value.minimum).getUTCFullYear()
  const lastYear = new Date(dateRange.value.maximum).getUTCFullYear()
  const yearSpan = Math.max(lastYear - firstYear, 1)
  const roughStep = yearSpan / 6
  const step = [1, 2, 5, 10, 20, 50].find((candidate) => candidate >= roughStep) ?? 100
  const ticks = []

  for (let year = Math.ceil(firstYear / step) * step; year <= lastYear; year += step) {
    const date = new Date(Date.UTC(year, 0, 1))
    ticks.push({ year, x: xFor(date) })
  }

  return ticks
})

const chartHeight = computed(() => chartTop + rows.value.length * rowHeight + chartBottom)
const statuses = computed(() => [...new Set(rows.value.map((row) => row.status))])
const instrumentTypes = computed(() => [...new Set(rows.value.map((row) => row.type))])
const currentDateX = computed(() => xFor(today))

function parseDate(value: string): Date | null {
  const parsed = new Date(`${value}T00:00:00Z`)
  return Number.isNaN(parsed.getTime()) ? null : parsed
}

function xFor(date: Date): number {
  const progress = (date.getTime() - dateRange.value.minimum) / dateRange.value.span
  return labelWidth + Math.max(0, Math.min(1, progress)) * plotWidth
}

function barWidth(row: ChartRow): number {
  return Math.max(4, xFor(row.end) - xFor(row.start))
}

function rowY(index: number): number {
  return chartTop + index * rowHeight
}

function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    timeZone: 'UTC'
  }).format(date)
}

function dateRangeLabel(row: ChartRow): string {
  return `${formatDate(row.start)} - ${row.isOngoing ? 'Present' : formatDate(row.end)}`
}

function normalize(value: string): string {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '') || 'other'
}

function statusColor(status: string): string {
  const colors: Record<string, string> = {
    operational: '#2da44e',
    planned: '#0969da',
    experimental: '#bf8700',
    retired: '#cf222e'
  }
  return colors[normalize(status)] ?? '#6e7781'
}

function patternId(type: string): string {
  const supported = ['multispectral', 'hyperspectral', 'radar', 'lidar', 'rgb']
  const normalized = normalize(type)
  return `timeline-pattern-${supported.includes(normalized) ? normalized : 'other'}`
}

function addInstrument() {
  if (!pendingId.value || selectedIds.value.includes(pendingId.value)) return
  selectedIds.value.push(pendingId.value)
  pendingId.value = ''
}

function removeInstrument(instrumentId: string) {
  if (instrumentId === props.instrumentId) return
  selectedIds.value = selectedIds.value.filter((id) => id !== instrumentId)
}
</script>

<template>
  <section class="timeline-section" aria-labelledby="timeline-title">
    <div class="timeline-heading">
      <div>
        <h3 id="timeline-title">Operational timeline</h3>
        <p>Compare this instrument's lifespan with other instruments in the catalogue.</p>
      </div>

      <form class="timeline-add" @submit.prevent="addInstrument">
        <label for="timeline-instrument-select">Add an instrument</label>
        <div>
          <select id="timeline-instrument-select" v-model="pendingId">
            <option value="">Select an instrument</option>
            <option
              v-for="instrument in availableInstruments"
              :key="instrument.id"
              :value="instrument.id"
            >
              {{ instrument.id }} - {{ instrument.timeline.name }}
            </option>
          </select>
          <button type="submit" :disabled="!pendingId">Add</button>
        </div>
      </form>
    </div>

    <ul class="timeline-selection" aria-label="Instruments shown in the timeline">
      <li
        v-for="row in rows"
        :key="row.id"
        :class="{ 'is-current': row.isCurrent }"
      >
        <span class="status-dot" :style="{ backgroundColor: statusColor(row.status) }" />
        <span>{{ row.id }}</span>
        <small v-if="row.isCurrent">Current</small>
        <button
          v-else
          type="button"
          :aria-label="`Remove ${row.id} from timeline`"
          title="Remove from timeline"
          @click="removeInstrument(row.id)"
        >
          &times;
        </button>
      </li>
    </ul>

    <div class="timeline-chart-scroll" tabindex="0" aria-label="Scrollable instrument timeline">
      <svg
        class="timeline-chart"
        :viewBox="`0 0 ${chartWidth} ${chartHeight}`"
        role="img"
        aria-labelledby="timeline-chart-title timeline-chart-description"
      >
        <title id="timeline-chart-title">Instrument operational timeline comparison</title>
        <desc id="timeline-chart-description">
          Bars show each selected instrument from its start date to its end date or the current date.
        </desc>

        <defs>
          <pattern id="timeline-pattern-multispectral" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
            <line x1="0" y1="0" x2="0" y2="12" class="pattern-line" />
          </pattern>
          <pattern id="timeline-pattern-hyperspectral" width="6" height="6" patternUnits="userSpaceOnUse">
            <line x1="3" y1="0" x2="3" y2="6" class="pattern-line" />
          </pattern>
          <pattern id="timeline-pattern-radar" width="10" height="10" patternUnits="userSpaceOnUse">
            <circle cx="3" cy="3" r="1.5" class="pattern-dot" />
            <circle cx="8" cy="8" r="1.5" class="pattern-dot" />
          </pattern>
          <pattern id="timeline-pattern-lidar" width="10" height="10" patternUnits="userSpaceOnUse">
            <path d="M0 5h10M5 0v10" class="pattern-line" />
          </pattern>
          <pattern id="timeline-pattern-rgb" width="9" height="9" patternUnits="userSpaceOnUse">
            <line x1="0" y1="4.5" x2="9" y2="4.5" class="pattern-line" />
          </pattern>
          <pattern id="timeline-pattern-other" width="12" height="12" patternUnits="userSpaceOnUse">
            <path d="M0 0l12 12M12 0L0 12" class="pattern-line" />
          </pattern>
          <filter id="timeline-current-glow" x="-35%" y="-100%" width="170%" height="300%">
            <feGaussianBlur stdDeviation="5" result="blur" />
            <feFlood flood-color="var(--vp-c-brand-1)" flood-opacity="0.65" />
            <feComposite in2="blur" operator="in" />
            <feMerge>
              <feMergeNode />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <g class="axis-grid">
          <g v-for="tick in axisTicks" :key="tick.year">
            <line
              :x1="tick.x"
              :x2="tick.x"
              :y1="chartTop - 16"
              :y2="chartHeight - chartBottom + 8"
            />
            <text :x="tick.x" :y="chartTop - 25" text-anchor="middle">{{ tick.year }}</text>
          </g>
        </g>

        <g v-if="currentDateX >= labelWidth && currentDateX <= chartWidth - chartRight" class="today-marker">
          <line
            :x1="currentDateX"
            :x2="currentDateX"
            :y1="chartTop - 16"
            :y2="chartHeight - chartBottom + 8"
          />
          <text :x="currentDateX - 5" :y="chartHeight - chartBottom + 28" text-anchor="end">Today</text>
        </g>

        <g
          v-for="(row, index) in rows"
          :key="row.id"
          class="timeline-row"
          :class="{ 'is-current': row.isCurrent }"
        >
          <title>{{ row.id }}: {{ dateRangeLabel(row) }}, {{ row.status }}, {{ row.type }}</title>
          <line
            :x1="labelWidth"
            :x2="chartWidth - chartRight"
            :y1="rowY(index) + 38"
            :y2="rowY(index) + 38"
            class="row-guide"
          />
          <text x="4" :y="rowY(index) + 18" class="row-label">
            {{ row.id }}
          </text>
          <text x="4" :y="rowY(index) + 38" class="row-dates">
            {{ dateRangeLabel(row) }}
          </text>
          <rect
            v-if="row.isCurrent"
            :x="xFor(row.start) - 4"
            :y="rowY(index) + 7"
            :width="barWidth(row) + 8"
            height="34"
            rx="11"
            class="current-outline"
            filter="url(#timeline-current-glow)"
          />
          <rect
            :x="xFor(row.start)"
            :y="rowY(index) + 11"
            :width="barWidth(row)"
            height="26"
            rx="8"
            :fill="statusColor(row.status)"
            class="timeline-bar"
          />
          <rect
            :x="xFor(row.start)"
            :y="rowY(index) + 11"
            :width="barWidth(row)"
            height="26"
            rx="8"
            :fill="`url(#${patternId(row.type)})`"
            class="timeline-texture"
          />
          <circle :cx="xFor(row.start)" :cy="rowY(index) + 24" r="4" class="date-cap" />
          <circle :cx="xFor(row.end)" :cy="rowY(index) + 24" r="4" class="date-cap" />
        </g>
      </svg>
    </div>

    <div class="timeline-legends">
      <div class="timeline-legend" aria-label="Status colors">
        <strong>Status</strong>
        <span v-for="status in statuses" :key="status">
          <i :style="{ backgroundColor: statusColor(status) }" />
          {{ status }}
        </span>
      </div>
      <div class="timeline-legend type-legend" aria-label="Instrument type textures">
        <strong>Type texture</strong>
        <span v-for="type in instrumentTypes" :key="type">
          <i :class="`texture-${normalize(type)}`" />
          {{ type }}
        </span>
      </div>
    </div>

    <p class="timeline-note">
      Instruments without an end date are shown through {{ formatDate(today) }}. The current page's instrument is outlined and marked as Current.
    </p>
  </section>
</template>

<style scoped>
.timeline-section {
  margin-top: 1.5rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 20px;
  padding: 1.1rem;
  background:
    radial-gradient(circle at 85% 0%, color-mix(in srgb, var(--vp-c-brand-1) 10%, transparent), transparent 38%),
    var(--vp-c-bg-soft);
}

.timeline-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 1.25rem;
}

.timeline-heading h3 {
  margin: 0;
  border: 0;
  padding: 0;
  font-size: 1.1rem;
}

.timeline-heading p {
  margin: 0.35rem 0 0;
  color: var(--vp-c-text-2);
  font-size: 0.9rem;
}

.timeline-add {
  flex: 0 1 410px;
}

.timeline-add label {
  display: block;
  margin-bottom: 0.35rem;
  color: var(--vp-c-text-2);
  font-size: 0.75rem;
  font-weight: 750;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.timeline-add > div {
  display: flex;
  gap: 0.45rem;
}

.timeline-add select {
  min-width: 0;
  flex: 1;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  padding: 0.55rem 0.7rem;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font: inherit;
  font-size: 0.84rem;
}

.timeline-add button {
  border: 0;
  border-radius: 10px;
  padding: 0.55rem 0.85rem;
  background: var(--vp-c-brand-1);
  color: var(--vp-c-bg);
  font: inherit;
  font-size: 0.84rem;
  font-weight: 750;
  cursor: pointer;
}

.timeline-add button:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}

.timeline-selection {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin: 1rem 0 0;
  padding: 0;
  list-style: none;
}

.timeline-selection li {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  padding: 0.3rem 0.45rem 0.3rem 0.55rem;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 0.76rem;
  font-weight: 700;
}

.timeline-selection li.is-current {
  border-color: color-mix(in srgb, var(--vp-c-brand-1) 65%, var(--vp-c-divider));
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--vp-c-brand-1) 12%, transparent);
}

.timeline-selection small {
  border-radius: 999px;
  padding: 0.1rem 0.4rem;
  background: color-mix(in srgb, var(--vp-c-brand-1) 15%, transparent);
  color: var(--vp-c-brand-1);
  font-size: 0.65rem;
  text-transform: uppercase;
}

.timeline-selection button {
  display: grid;
  width: 1.25rem;
  height: 1.25rem;
  place-items: center;
  border: 0;
  border-radius: 50%;
  padding: 0;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-2);
  font: inherit;
  font-size: 1rem;
  line-height: 1;
  cursor: pointer;
}

.timeline-selection button:hover {
  background: color-mix(in srgb, #cf222e 15%, transparent);
  color: #cf222e;
}

.status-dot {
  width: 0.55rem;
  height: 0.55rem;
  border-radius: 50%;
}

.timeline-chart-scroll {
  overflow-x: auto;
  margin-top: 0.85rem;
  border: 1px solid color-mix(in srgb, var(--vp-c-divider) 75%, transparent);
  border-radius: 14px;
  background: color-mix(in srgb, var(--vp-c-bg) 82%, transparent);
  scrollbar-width: thin;
}

.timeline-chart-scroll:focus-visible,
.timeline-add select:focus-visible,
.timeline-add button:focus-visible,
.timeline-selection button:focus-visible {
  outline: 2px solid var(--vp-c-brand-1);
  outline-offset: 2px;
}

.timeline-chart {
  display: block;
  width: 100%;
  min-width: 860px;
  height: auto;
  font-family: var(--vp-font-family-base);
}

.axis-grid line {
  stroke: var(--vp-c-divider);
  stroke-width: 1;
  stroke-dasharray: 3 6;
}

.axis-grid text,
.today-marker text {
  fill: var(--vp-c-text-3);
  font-size: 12px;
  font-weight: 650;
}

.today-marker line {
  stroke: var(--vp-c-brand-1);
  stroke-width: 1.5;
  stroke-dasharray: 4 4;
}

.row-guide {
  stroke: var(--vp-c-divider);
  stroke-width: 1;
}

.row-label {
  fill: var(--vp-c-text-1);
  font-size: 15px;
  font-weight: 760;
}

.row-dates {
  fill: var(--vp-c-text-3);
  font-size: 11px;
}

.timeline-bar {
  stroke: color-mix(in srgb, var(--vp-c-text-1) 25%, transparent);
  stroke-width: 1;
}

.timeline-texture {
  pointer-events: none;
}

.pattern-line {
  fill: none;
  stroke: var(--vp-c-bg);
  stroke-width: 3;
  opacity: 0.42;
}

.pattern-dot {
  fill: var(--vp-c-bg);
  opacity: 0.5;
}

.date-cap {
  fill: var(--vp-c-bg);
  stroke: var(--vp-c-text-1);
  stroke-width: 1.5;
}

.current-outline {
  fill: none;
  stroke: var(--vp-c-brand-1);
  stroke-width: 2.5;
}

.timeline-legends {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7rem 1.5rem;
  margin-top: 0.9rem;
}

.timeline-legend {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.45rem 0.8rem;
  color: var(--vp-c-text-2);
  font-size: 0.75rem;
  text-transform: capitalize;
}

.timeline-legend strong {
  color: var(--vp-c-text-1);
  font-size: 0.72rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.timeline-legend span {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.timeline-legend i {
  width: 1.4rem;
  height: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 3px;
}

.type-legend i {
  background-color: var(--vp-c-text-3);
}

.texture-multispectral {
  background-image: repeating-linear-gradient(35deg, transparent 0 4px, var(--vp-c-bg) 4px 6px);
}

.texture-hyperspectral {
  background-image: repeating-linear-gradient(90deg, transparent 0 3px, var(--vp-c-bg) 3px 4px);
}

.texture-radar {
  background-image: radial-gradient(var(--vp-c-bg) 1px, transparent 1.5px);
  background-size: 5px 5px;
}

.texture-lidar {
  background-image:
    linear-gradient(var(--vp-c-bg) 1px, transparent 1px),
    linear-gradient(90deg, var(--vp-c-bg) 1px, transparent 1px);
  background-size: 6px 6px;
}

.texture-rgb {
  background-image: repeating-linear-gradient(0deg, transparent 0 3px, var(--vp-c-bg) 3px 4px);
}

.texture-other {
  background-image:
    repeating-linear-gradient(45deg, transparent 0 5px, var(--vp-c-bg) 5px 6px),
    repeating-linear-gradient(-45deg, transparent 0 5px, var(--vp-c-bg) 5px 6px);
}

.timeline-note {
  margin: 0.8rem 0 0;
  color: var(--vp-c-text-3);
  font-size: 0.75rem;
}

@media (max-width: 760px) {
  .timeline-section {
    padding: 0.85rem;
  }

  .timeline-heading {
    display: grid;
    align-items: stretch;
  }

  .timeline-add {
    width: 100%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .current-outline {
    filter: none;
  }
}
</style>
