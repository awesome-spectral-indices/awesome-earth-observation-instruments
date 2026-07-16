<script setup lang="ts">
import { computed, ref, shallowRef } from 'vue'
import spectralData from '../../data/spectral-comparison.json'

type BandInterval = {
  id: string
  start: number
  end: number
  center: number
}

type ResponseCurve = {
  id: string
  points: [number, number][]
  peak: [number, number]
}

type SpectralInstrument = {
  id: string
  name: string
  acronym: string
  bands: BandInterval[]
}

type ResponseInstrument = SpectralInstrument & {
  srf: ResponseCurve[]
}

type PackedBand = BandInterval & {
  lane: number
}

type BandRow = SpectralInstrument & {
  bands: PackedBand[]
  laneCount: number
  y: number
  height: number
  isCurrent: boolean
}

type HoveredBand = {
  instrumentId: string
  bandId: string
  range: string
  x: number
  y: number
}

type ZoomRange = {
  minimum: number
  maximum: number
}

type DragSelection = {
  mode: 'bands' | 'srf'
  startX: number
  currentX: number
}

const props = defineProps<{
  instrumentId: string
}>()

const instruments = spectralData as Record<string, SpectralInstrument>
const defaultComparisons = ['MSI_S2A', 'ETM_L7', 'OLI2_L9']
const fallbackComparison = 'TM_L5'
const colors = ['#0072b2', '#d55e00', '#009e73', '#cc79a7', '#e69f00', '#56b4e9', '#7b61a8', '#8c6d31']

const chartWidth = 1040
const bandLabelWidth = 238
const chartRight = 28
const bandPlotWidth = chartWidth - bandLabelWidth - chartRight
const bandTop = 62
const bandBottom = 60
const srfLeft = 72
const srfTop = 58
const srfBottom = 62
const srfHeight = 500
const srfPlotWidth = chartWidth - srfLeft - chartRight
const srfPlotHeight = srfHeight - srfTop - srfBottom

const initialIds = [
  props.instrumentId,
  ...defaultComparisons.filter((id) => id !== props.instrumentId)
]

if (defaultComparisons.includes(props.instrumentId)) {
  initialIds.push(fallbackComparison)
}

const selectedIds = ref([...new Set(initialIds.filter((id) => instruments[id]?.bands.length))])
const pendingId = ref('')
const view = ref<'bands' | 'srf'>('bands')
const hoveredBand = ref<HoveredBand | null>(null)
const bandZoom = ref<ZoomRange | null>(null)
const responseZoom = ref<ZoomRange | null>(null)
const bandZoomMinimum = ref('')
const bandZoomMaximum = ref('')
const responseZoomMinimum = ref('')
const responseZoomMaximum = ref('')
const zoomError = ref('')
const dragSelection = ref<DragSelection | null>(null)
const responseData = shallowRef<Record<string, ResponseCurve[]>>({})
const responseLoading = ref(false)
const responseLoaded = ref(false)
const responseLoadError = ref('')

const selectedInstruments = computed(() =>
  selectedIds.value.flatMap((id) => instruments[id] ? [instruments[id]] : [])
)

const availableInstruments = computed(() =>
  Object.values(instruments)
    .filter((instrument) => instrument.bands.length && !selectedIds.value.includes(instrument.id))
    .sort((left, right) => left.id.localeCompare(right.id))
)

const wavelengthRange = computed(() => {
  const intervals = selectedInstruments.value.flatMap((instrument) => instrument.bands)
  if (!intervals.length) return { minimum: 0, maximum: 1, span: 1 }

  const minimum = Math.min(...intervals.map((band) => band.start))
  const maximum = Math.max(...intervals.map((band) => band.end))
  return { minimum, maximum, span: Math.max(maximum - minimum, 1) }
})

const bandDisplayRange = computed(() =>
  resolvedZoomRange(bandZoom.value, wavelengthRange.value)
)

const bandRows = computed<BandRow[]>(() => {
  let y = bandTop

  return selectedInstruments.value.map((instrument) => {
    const laneEnds: number[] = []
    const bands = [...instrument.bands]
      .sort((left, right) => left.start - right.start || left.end - right.end)
      .map((band) => {
        let lane = laneEnds.findIndex((end) => band.start >= end)
        if (lane < 0) {
          lane = laneEnds.length
          laneEnds.push(band.end)
        } else {
          laneEnds[lane] = band.end
        }
        return { ...band, lane }
      })

    const laneCount = Math.max(laneEnds.length, 1)
    const height = Math.max(58, 24 + laneCount * 22)
    const row = {
      ...instrument,
      bands,
      laneCount,
      y,
      height,
      isCurrent: instrument.id === props.instrumentId
    }
    y += height
    return row
  })
})

const bandChartHeight = computed(() =>
  bandTop + bandRows.value.reduce((total, row) => total + row.height, 0) + bandBottom
)

const bandTicks = computed(() => niceTicks(bandDisplayRange.value.minimum, bandDisplayRange.value.maximum, 7))

const responseInstruments = computed<ResponseInstrument[]>(() =>
  selectedInstruments.value
    .filter((instrument) => responseData.value[instrument.id]?.length)
    .map((instrument) => ({ ...instrument, srf: responseData.value[instrument.id] }))
    .sort((left, right) => Number(left.id === props.instrumentId) - Number(right.id === props.instrumentId))
)

const unavailableSrf = computed(() =>
  selectedInstruments.value.filter((instrument) => !responseData.value[instrument.id]?.length)
)

const responseRange = computed(() => {
  const points = responseInstruments.value.flatMap((instrument) =>
    instrument.srf.flatMap((curve) => curve.points)
  )
  if (!points.length) {
    return { xMin: 0, xMax: 1, xSpan: 1, yMin: 0, yMax: 1, ySpan: 1 }
  }

  const xMin = Math.min(...points.map((point) => point[0]))
  const xMax = Math.max(...points.map((point) => point[0]))
  const minimumResponse = Math.min(...points.map((point) => point[1]))
  const maximumResponse = Math.max(...points.map((point) => point[1]))
  const yMin = minimumResponse < 0 ? Math.floor(minimumResponse * 20) / 20 : 0
  const yMax = Math.max(1, Math.ceil(maximumResponse * 20) / 20)

  return {
    xMin,
    xMax,
    xSpan: Math.max(xMax - xMin, 1),
    yMin,
    yMax,
    ySpan: Math.max(yMax - yMin, 0.01)
  }
})

const responseFullRange = computed(() => ({
  minimum: responseRange.value.xMin,
  maximum: responseRange.value.xMax,
  span: responseRange.value.xSpan
}))
const responseDisplayRange = computed(() =>
  resolvedZoomRange(responseZoom.value, responseFullRange.value)
)
const responseXTicks = computed(() => niceTicks(responseDisplayRange.value.minimum, responseDisplayRange.value.maximum, 7))
const responseYTicks = computed(() => niceTicks(responseRange.value.yMin, responseRange.value.yMax, 5))
const activeFullRange = computed(() =>
  view.value === 'bands' ? wavelengthRange.value : responseFullRange.value
)
const activeDisplayRange = computed(() =>
  view.value === 'bands' ? bandDisplayRange.value : responseDisplayRange.value
)
const isZoomed = computed(() =>
  view.value === 'bands' ? bandZoom.value !== null : responseZoom.value !== null
)
const zoomMinimumInput = computed({
  get: () => view.value === 'bands' ? bandZoomMinimum.value : responseZoomMinimum.value,
  set: (value: string) => {
    if (view.value === 'bands') bandZoomMinimum.value = value
    else responseZoomMinimum.value = value
  }
})
const zoomMaximumInput = computed({
  get: () => view.value === 'bands' ? bandZoomMaximum.value : responseZoomMaximum.value,
  set: (value: string) => {
    if (view.value === 'bands') bandZoomMaximum.value = value
    else responseZoomMaximum.value = value
  }
})

function niceTicks(minimum: number, maximum: number, targetCount: number): number[] {
  const range = Math.max(maximum - minimum, Number.EPSILON)
  const roughStep = range / targetCount
  const magnitude = 10 ** Math.floor(Math.log10(roughStep))
  const residual = roughStep / magnitude
  const multiplier = residual <= 1 ? 1 : residual <= 2 ? 2 : residual <= 5 ? 5 : 10
  const step = multiplier * magnitude
  const first = Math.ceil(minimum / step) * step
  const ticks = []

  for (let value = first; value <= maximum + step * 0.001; value += step) {
    ticks.push(Number(value.toPrecision(12)))
  }
  return ticks
}

function resolvedZoomRange(
  zoom: ZoomRange | null,
  fullRange: { minimum: number, maximum: number, span: number }
): ZoomRange & { span: number } {
  if (!zoom) return fullRange

  const minimum = Math.max(fullRange.minimum, zoom.minimum)
  const maximum = Math.min(fullRange.maximum, zoom.maximum)
  if (minimum >= maximum) return fullRange

  return { minimum, maximum, span: maximum - minimum }
}

function bandX(wavelength: number): number {
  const progress = (wavelength - bandDisplayRange.value.minimum) / bandDisplayRange.value.span
  return bandLabelWidth + progress * bandPlotWidth
}

function responseX(wavelength: number): number {
  const progress = (wavelength - responseDisplayRange.value.minimum) / responseDisplayRange.value.span
  return srfLeft + progress * srfPlotWidth
}

function responseY(response: number): number {
  const progress = (response - responseRange.value.yMin) / responseRange.value.ySpan
  return srfTop + srfPlotHeight - progress * srfPlotHeight
}

function responsePath(points: [number, number][]): string {
  return points
    .map((point, index) => `${index ? 'L' : 'M'}${responseX(point[0]).toFixed(2)},${responseY(point[1]).toFixed(2)}`)
    .join(' ')
}

function instrumentColor(instrumentId: string): string {
  const index = selectedIds.value.indexOf(instrumentId)
  return colors[(index < 0 ? 0 : index) % colors.length]
}

function formatWavelength(value: number): string {
  return new Intl.NumberFormat('en', { maximumFractionDigits: value < 10 ? 2 : 0 }).format(value)
}

function bandRange(band: BandInterval): string {
  return `${formatWavelength(band.start)}-${formatWavelength(band.end)} nm`
}

function showBand(row: BandRow, band: PackedBand) {
  const centerX = bandX((band.start + band.end) / 2)
  hoveredBand.value = {
    instrumentId: row.id,
    bandId: band.id,
    range: bandRange(band),
    x: Math.max(bandLabelWidth + 82, Math.min(chartWidth - chartRight - 82, centerX)),
    y: Math.max(48, row.y + 10 + band.lane * 22)
  }
}

function annotationY(curve: ResponseCurve, instrumentIndex: number): number {
  const peakY = responseY(curve.peak[1])
  if (peakY < srfTop + 70) return peakY + 14 + instrumentIndex * 12
  return peakY - 8 - instrumentIndex * 12
}

function selectView(nextView: 'bands' | 'srf') {
  view.value = nextView
  zoomError.value = ''
  dragSelection.value = null
  if (nextView === 'srf') void loadResponseData()
}

async function loadResponseData() {
  if (responseLoaded.value || responseLoading.value) return

  responseLoading.value = true
  responseLoadError.value = ''
  try {
    const module = await import('../../data/spectral-response-functions.json')
    responseData.value = module.default as Record<string, ResponseCurve[]>
    responseLoaded.value = true
  } catch {
    responseLoadError.value = 'The spectral response function data could not be loaded.'
  } finally {
    responseLoading.value = false
  }
}

function applyZoom() {
  const minimum = Number(zoomMinimumInput.value)
  const maximum = Number(zoomMaximumInput.value)

  if (!Number.isFinite(minimum) || !Number.isFinite(maximum) || minimum >= maximum) {
    zoomError.value = 'Enter a valid minimum wavelength below the maximum wavelength.'
    return
  }

  applyZoomRange(view.value, minimum, maximum)
}

function applyZoomRange(mode: 'bands' | 'srf', requestedMinimum: number, requestedMaximum: number) {
  const fullRange = mode === 'bands' ? wavelengthRange.value : responseFullRange.value
  const minimum = Math.max(fullRange.minimum, requestedMinimum)
  const maximum = Math.min(fullRange.maximum, requestedMaximum)

  if (minimum >= maximum) {
    zoomError.value = 'The requested range does not overlap the available wavelengths.'
    return
  }

  const zoom = { minimum, maximum }
  if (mode === 'bands') {
    bandZoom.value = zoom
    bandZoomMinimum.value = String(Number(minimum.toFixed(3)))
    bandZoomMaximum.value = String(Number(maximum.toFixed(3)))
  } else {
    responseZoom.value = zoom
    responseZoomMinimum.value = String(Number(minimum.toFixed(3)))
    responseZoomMaximum.value = String(Number(maximum.toFixed(3)))
  }
  zoomError.value = ''
}

function resetZoom() {
  if (view.value === 'bands') {
    bandZoom.value = null
    bandZoomMinimum.value = ''
    bandZoomMaximum.value = ''
  } else {
    responseZoom.value = null
    responseZoomMinimum.value = ''
    responseZoomMaximum.value = ''
  }
  zoomError.value = ''
  dragSelection.value = null
}

function svgCoordinates(event: PointerEvent, svg: SVGSVGElement) {
  const bounds = svg.getBoundingClientRect()
  const scale = chartWidth / bounds.width
  return {
    x: (event.clientX - bounds.left) * scale,
    y: (event.clientY - bounds.top) * scale
  }
}

function beginZoomDrag(event: PointerEvent, mode: 'bands' | 'srf') {
  if (event.button !== 0) return

  const svg = event.currentTarget as SVGSVGElement
  const point = svgCoordinates(event, svg)
  const left = mode === 'bands' ? bandLabelWidth : srfLeft
  const right = chartWidth - chartRight
  const top = mode === 'bands' ? bandTop - 14 : srfTop
  const bottom = mode === 'bands' ? bandChartHeight.value - bandBottom + 6 : srfTop + srfPlotHeight
  if (point.x < left || point.x > right || point.y < top || point.y > bottom) return

  svg.setPointerCapture(event.pointerId)
  dragSelection.value = { mode, startX: point.x, currentX: point.x }
  hoveredBand.value = null
}

function updateZoomDrag(event: PointerEvent) {
  if (!dragSelection.value) return

  const svg = event.currentTarget as SVGSVGElement
  const point = svgCoordinates(event, svg)
  const left = dragSelection.value.mode === 'bands' ? bandLabelWidth : srfLeft
  const right = chartWidth - chartRight
  dragSelection.value.currentX = Math.max(left, Math.min(right, point.x))
}

function finishZoomDrag(event: PointerEvent) {
  const selection = dragSelection.value
  if (!selection) return

  const svg = event.currentTarget as SVGSVGElement
  if (svg.hasPointerCapture(event.pointerId)) svg.releasePointerCapture(event.pointerId)
  dragSelection.value = null

  if (Math.abs(selection.currentX - selection.startX) < 8) return

  const left = selection.mode === 'bands' ? bandLabelWidth : srfLeft
  const width = selection.mode === 'bands' ? bandPlotWidth : srfPlotWidth
  const range = selection.mode === 'bands' ? bandDisplayRange.value : responseDisplayRange.value
  const selectionMinimum = Math.min(selection.startX, selection.currentX)
  const selectionMaximum = Math.max(selection.startX, selection.currentX)
  const minimum = range.minimum + ((selectionMinimum - left) / width) * range.span
  const maximum = range.minimum + ((selectionMaximum - left) / width) * range.span
  applyZoomRange(selection.mode, minimum, maximum)
}

function cancelZoomDrag() {
  dragSelection.value = null
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
  <section class="spectral-comparison" aria-labelledby="spectral-comparison-title">
    <div class="comparison-heading">
      <div>
        <h3 id="spectral-comparison-title">Spectral comparison</h3>
        <p>Compare band coverage or spectral response functions across catalogue instruments.</p>
      </div>

      <div class="view-switch" role="group" aria-label="Spectral figure type">
        <button type="button" :aria-pressed="view === 'bands'" @click="selectView('bands')">Band coverage</button>
        <button type="button" :aria-pressed="view === 'srf'" @click="selectView('srf')">Response functions</button>
      </div>
    </div>

    <form class="comparison-add" @submit.prevent="addInstrument">
      <label for="spectral-instrument-select">Add an instrument</label>
      <div>
        <select id="spectral-instrument-select" v-model="pendingId">
          <option value="">Select an instrument</option>
          <option
            v-for="instrument in availableInstruments"
            :key="instrument.id"
            :value="instrument.id"
          >
            {{ instrument.id }} - {{ instrument.name }}
          </option>
        </select>
        <button type="submit" :disabled="!pendingId">Add</button>
      </div>
    </form>

    <ul class="comparison-selection" aria-label="Instruments shown in the spectral figure">
      <li
        v-for="instrument in selectedInstruments"
        :key="instrument.id"
        :class="{ 'is-current': instrument.id === props.instrumentId }"
      >
        <span class="color-dot" :style="{ backgroundColor: instrumentColor(instrument.id) }" />
        <span>{{ instrument.id }}</span>
        <small v-if="instrument.id === props.instrumentId">Current</small>
        <button
          v-else
          type="button"
          :aria-label="`Remove ${instrument.id} from spectral comparison`"
          title="Remove from comparison"
          @click="removeInstrument(instrument.id)"
        >
          &times;
        </button>
      </li>
    </ul>

    <form v-if="view === 'bands' || responseLoaded" class="zoom-controls" @submit.prevent="applyZoom">
      <div class="zoom-label">
        <strong>X-axis zoom</strong>
        <span>Drag across the plot or enter a wavelength range.</span>
      </div>
      <label>
        <span>Minimum (nm)</span>
        <input
          v-model="zoomMinimumInput"
          type="number"
          step="any"
          :min="activeFullRange.minimum"
          :max="activeFullRange.maximum"
          :placeholder="String(Number(activeFullRange.minimum.toFixed(2)))"
        >
      </label>
      <label>
        <span>Maximum (nm)</span>
        <input
          v-model="zoomMaximumInput"
          type="number"
          step="any"
          :min="activeFullRange.minimum"
          :max="activeFullRange.maximum"
          :placeholder="String(Number(activeFullRange.maximum.toFixed(2)))"
        >
      </label>
      <button type="submit">Apply</button>
      <button type="button" class="reset-zoom" :disabled="!isZoomed" @click="resetZoom">Reset</button>
      <output class="zoom-readout" aria-live="polite">
        {{ formatWavelength(activeDisplayRange.minimum) }}-{{ formatWavelength(activeDisplayRange.maximum) }} nm
      </output>
    </form>
    <p v-if="zoomError" class="zoom-error" role="alert">{{ zoomError }}</p>

    <div
      v-if="view === 'bands'"
      class="chart-scroll"
      tabindex="0"
      aria-label="Scrollable spectral band coverage chart"
    >
      <svg
        class="spectral-chart band-chart"
        :viewBox="`0 0 ${chartWidth} ${bandChartHeight}`"
        role="img"
        aria-labelledby="band-chart-title band-chart-description"
        @mouseleave="hoveredBand = null"
        @pointerdown="beginZoomDrag($event, 'bands')"
        @pointermove="updateZoomDrag"
        @pointerup="finishZoomDrag"
        @pointercancel="cancelZoomDrag"
      >
        <title id="band-chart-title">Spectral band coverage comparison</title>
        <desc id="band-chart-description">
          Each instrument row shows band start and end wavelengths. Overlapping bands use separate compact lanes.
        </desc>

        <defs>
          <filter id="spectral-band-glow" x="-20%" y="-60%" width="140%" height="220%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feFlood flood-color="var(--vp-c-brand-1)" flood-opacity="0.5" />
            <feComposite in2="blur" operator="in" />
            <feMerge><feMergeNode /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
          <clipPath id="band-plot-clip">
            <rect
              :x="bandLabelWidth"
              :y="bandTop - 14"
              :width="bandPlotWidth"
              :height="bandChartHeight - bandTop - bandBottom + 20"
            />
          </clipPath>
        </defs>

        <g class="chart-grid">
          <g v-for="tick in bandTicks" :key="tick">
            <line :x1="bandX(tick)" :x2="bandX(tick)" :y1="bandTop - 14" :y2="bandChartHeight - bandBottom + 6" />
            <text :x="bandX(tick)" :y="bandTop - 25" text-anchor="middle">{{ formatWavelength(tick) }}</text>
          </g>
          <text :x="chartWidth - chartRight" :y="bandChartHeight - 18" text-anchor="end" class="axis-label">Wavelength (nm)</text>
        </g>

        <g v-for="row in bandRows" :key="row.id" class="band-row">
          <rect
            v-if="row.isCurrent"
            x="9"
            :y="row.y + 2"
            :width="chartWidth - 18"
            :height="row.height - 4"
            rx="12"
            class="current-row"
            filter="url(#spectral-band-glow)"
          />
          <line x1="10" :x2="chartWidth - 10" :y1="row.y + row.height" :y2="row.y + row.height" class="row-divider" />
          <text x="18" :y="row.y + row.height / 2 - 3" class="instrument-label">{{ row.id }}</text>
          <text x="18" :y="row.y + row.height / 2 + 15" class="instrument-detail">{{ row.bands.length }} bands</text>

          <g
            v-for="band in row.bands"
            :key="band.id"
            class="band-mark"
            tabindex="0"
            clip-path="url(#band-plot-clip)"
            @mouseenter="showBand(row, band)"
            @focus="showBand(row, band)"
            @mouseleave="hoveredBand = null"
            @blur="hoveredBand = null"
          >
            <title>{{ row.id }} {{ band.id }}: {{ bandRange(band) }}</title>
            <rect
              :x="bandX(band.start)"
              :y="row.y + 10 + band.lane * 22"
              :width="Math.max(3, bandX(band.end) - bandX(band.start))"
              height="15"
              rx="4"
              :fill="instrumentColor(row.id)"
              :class="{ 'is-current': row.isCurrent }"
            />
          </g>
        </g>

        <rect
          v-if="dragSelection?.mode === 'bands'"
          :x="Math.min(dragSelection.startX, dragSelection.currentX)"
          :y="bandTop - 14"
          :width="Math.abs(dragSelection.currentX - dragSelection.startX)"
          :height="bandChartHeight - bandTop - bandBottom + 20"
          class="zoom-selection"
          pointer-events="none"
        />

        <g v-if="hoveredBand" class="band-tooltip" pointer-events="none">
          <rect :x="hoveredBand.x - 78" :y="hoveredBand.y - 44" width="156" height="39" rx="7" />
          <text :x="hoveredBand.x" :y="hoveredBand.y - 28" text-anchor="middle">{{ hoveredBand.instrumentId }} · {{ hoveredBand.bandId }}</text>
          <text :x="hoveredBand.x" :y="hoveredBand.y - 14" text-anchor="middle" class="tooltip-range">{{ hoveredBand.range }}</text>
        </g>
      </svg>
    </div>

    <div v-else class="srf-view">
      <p v-if="responseLoading" class="empty-state">Loading full-resolution spectral response functions...</p>
      <p v-else-if="responseLoadError" class="zoom-error" role="alert">{{ responseLoadError }}</p>

      <div v-else-if="responseInstruments.length" class="chart-scroll" tabindex="0" aria-label="Scrollable spectral response function chart">
        <svg
          class="spectral-chart srf-chart"
          :viewBox="`0 0 ${chartWidth} ${srfHeight}`"
          role="img"
          aria-labelledby="srf-chart-title srf-chart-description"
          @pointerdown="beginZoomDrag($event, 'srf')"
          @pointermove="updateZoomDrag"
          @pointerup="finishZoomDrag"
          @pointercancel="cancelZoomDrag"
        >
          <title id="srf-chart-title">Spectral response function comparison</title>
          <desc id="srf-chart-description">
            Spectral response curves use one color per instrument and labels mark individual bands.
          </desc>

          <defs>
            <filter id="spectral-curve-glow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feFlood flood-color="var(--vp-c-brand-1)" flood-opacity="0.7" />
              <feComposite in2="blur" operator="in" />
              <feMerge><feMergeNode /><feMergeNode in="SourceGraphic" /></feMerge>
            </filter>
            <clipPath id="srf-plot-clip">
              <rect :x="srfLeft" :y="srfTop" :width="srfPlotWidth" :height="srfPlotHeight" />
            </clipPath>
          </defs>

          <g class="chart-grid">
            <g v-for="tick in responseXTicks" :key="`x-${tick}`">
              <line :x1="responseX(tick)" :x2="responseX(tick)" :y1="srfTop" :y2="srfTop + srfPlotHeight" />
              <text :x="responseX(tick)" :y="srfHeight - srfBottom + 24" text-anchor="middle">{{ formatWavelength(tick) }}</text>
            </g>
            <g v-for="tick in responseYTicks" :key="`y-${tick}`">
              <line :x1="srfLeft" :x2="chartWidth - chartRight" :y1="responseY(tick)" :y2="responseY(tick)" />
              <text :x="srfLeft - 10" :y="responseY(tick) + 4" text-anchor="end">{{ tick.toFixed(2) }}</text>
            </g>
          </g>

          <line :x1="srfLeft" :x2="srfLeft" :y1="srfTop" :y2="srfTop + srfPlotHeight" class="axis-line" />
          <line :x1="srfLeft" :x2="chartWidth - chartRight" :y1="srfTop + srfPlotHeight" :y2="srfTop + srfPlotHeight" class="axis-line" />
          <text :x="chartWidth - chartRight" :y="srfHeight - 14" text-anchor="end" class="axis-label">Wavelength (nm)</text>
          <text :x="18" :y="srfTop + srfPlotHeight / 2" text-anchor="middle" class="axis-label" transform="rotate(-90 18 248)">Response</text>

          <g clip-path="url(#srf-plot-clip)">
            <g
              v-for="(instrument, instrumentIndex) in responseInstruments"
              :key="instrument.id"
              class="response-instrument"
            >
              <path
                v-for="curve in instrument.srf"
                :key="curve.id"
                :d="responsePath(curve.points)"
                fill="none"
                :stroke="instrumentColor(instrument.id)"
                :class="{ 'is-current': instrument.id === props.instrumentId }"
                :filter="instrument.id === props.instrumentId ? 'url(#spectral-curve-glow)' : undefined"
              >
                <title>{{ instrument.id }} {{ curve.id }}</title>
              </path>
              <text
                v-for="curve in instrument.srf"
                :key="`label-${curve.id}`"
                :x="responseX(curve.peak[0])"
                :y="annotationY(curve, instrumentIndex)"
                text-anchor="middle"
                :fill="instrumentColor(instrument.id)"
                :class="{ 'is-current': instrument.id === props.instrumentId }"
                class="band-annotation"
              >
                {{ curve.id }}
              </text>
            </g>
          </g>
          <rect
            v-if="dragSelection?.mode === 'srf'"
            :x="Math.min(dragSelection.startX, dragSelection.currentX)"
            :y="srfTop"
            :width="Math.abs(dragSelection.currentX - dragSelection.startX)"
            :height="srfPlotHeight"
            class="zoom-selection"
            pointer-events="none"
          />
        </svg>
      </div>

      <p v-else-if="responseLoaded" class="empty-state">None of the selected instruments has a spectral response function.</p>

      <p v-if="responseLoaded && unavailableSrf.length" class="availability-note">
        SRF not available for: {{ unavailableSrf.map((instrument) => instrument.id).join(', ') }}.
      </p>
    </div>

    <div class="instrument-legend" aria-label="Instrument colors">
      <strong>Instrument</strong>
      <span v-for="instrument in selectedInstruments" :key="instrument.id">
        <i :style="{ backgroundColor: instrumentColor(instrument.id) }" />
        {{ instrument.id }}
      </span>
    </div>

    <p class="comparison-note">
      The current instrument is highlighted. Overlapping band intervals are placed in compact lanes within the same instrument row.
    </p>
  </section>
</template>

<style scoped>
.spectral-comparison {
  margin-top: 1.5rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 20px;
  padding: 1.1rem;
  background:
    radial-gradient(circle at 86% 0%, color-mix(in srgb, var(--vp-c-brand-1) 10%, transparent), transparent 38%),
    var(--vp-c-bg-soft);
}

.comparison-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 1rem;
}

.comparison-heading h3 {
  margin: 0;
  border: 0;
  padding: 0;
  font-size: 1.1rem;
}

.comparison-heading p {
  margin: 0.35rem 0 0;
  color: var(--vp-c-text-2);
  font-size: 0.9rem;
}

.view-switch {
  display: inline-flex;
  flex: 0 0 auto;
  gap: 0.25rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 0.25rem;
  background: var(--vp-c-bg);
}

.view-switch button {
  border: 0;
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  background: transparent;
  color: var(--vp-c-text-2);
  font: inherit;
  font-size: 0.8rem;
  font-weight: 750;
  cursor: pointer;
}

.view-switch button[aria-pressed='true'] {
  background: color-mix(in srgb, var(--vp-c-brand-1) 15%, var(--vp-c-bg));
  color: var(--vp-c-brand-1);
}

.comparison-add {
  max-width: 520px;
  margin-top: 1rem;
}

.comparison-add label {
  display: block;
  margin-bottom: 0.35rem;
  color: var(--vp-c-text-2);
  font-size: 0.75rem;
  font-weight: 750;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.comparison-add > div {
  display: flex;
  gap: 0.45rem;
}

.comparison-add select {
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

.comparison-add button {
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

.comparison-add button:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}

.comparison-selection {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin: 0.9rem 0 0;
  padding: 0;
  list-style: none;
}

.comparison-selection li {
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

.comparison-selection li.is-current {
  border-color: color-mix(in srgb, var(--vp-c-brand-1) 65%, var(--vp-c-divider));
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--vp-c-brand-1) 12%, transparent);
}

.comparison-selection small {
  border-radius: 999px;
  padding: 0.1rem 0.4rem;
  background: color-mix(in srgb, var(--vp-c-brand-1) 15%, transparent);
  color: var(--vp-c-brand-1);
  font-size: 0.65rem;
  text-transform: uppercase;
}

.comparison-selection button {
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

.comparison-selection button:hover {
  background: color-mix(in srgb, #cf222e 15%, transparent);
  color: #cf222e;
}

.color-dot {
  width: 0.55rem;
  height: 0.55rem;
  border-radius: 50%;
}

.zoom-controls {
  display: grid;
  grid-template-columns: minmax(180px, 1fr) repeat(2, minmax(110px, 145px)) auto auto auto;
  align-items: end;
  gap: 0.55rem;
  margin-top: 0.9rem;
  border-top: 1px solid var(--vp-c-divider);
  padding-top: 0.85rem;
}

.zoom-label strong,
.zoom-controls label span {
  display: block;
  color: var(--vp-c-text-1);
  font-size: 0.72rem;
  font-weight: 750;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.zoom-label span {
  display: block;
  margin-top: 0.25rem;
  color: var(--vp-c-text-3);
  font-size: 0.72rem;
}

.zoom-controls input {
  width: 100%;
  margin-top: 0.3rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 9px;
  padding: 0.5rem 0.6rem;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font: inherit;
  font-size: 0.8rem;
}

.zoom-controls button {
  border: 0;
  border-radius: 9px;
  padding: 0.52rem 0.7rem;
  background: var(--vp-c-brand-1);
  color: var(--vp-c-bg);
  font: inherit;
  font-size: 0.78rem;
  font-weight: 750;
  cursor: pointer;
}

.zoom-controls .reset-zoom {
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-2);
}

.zoom-controls button:disabled {
  cursor: not-allowed;
  opacity: 0.42;
}

.zoom-readout {
  align-self: center;
  border-radius: 999px;
  padding: 0.28rem 0.55rem;
  background: color-mix(in srgb, var(--vp-c-brand-1) 11%, transparent);
  color: var(--vp-c-brand-1);
  font-size: 0.7rem;
  font-weight: 750;
  white-space: nowrap;
}

.zoom-error {
  margin: 0.45rem 0 0;
  color: #cf222e;
  font-size: 0.78rem;
  font-weight: 650;
}

.chart-scroll {
  overflow-x: auto;
  margin-top: 0.85rem;
  border: 1px solid color-mix(in srgb, var(--vp-c-divider) 75%, transparent);
  border-radius: 14px;
  background: color-mix(in srgb, var(--vp-c-bg) 84%, transparent);
  scrollbar-width: thin;
}

.chart-scroll:focus-visible,
.comparison-add select:focus-visible,
.comparison-add button:focus-visible,
.comparison-selection button:focus-visible,
.view-switch button:focus-visible,
.zoom-controls input:focus-visible,
.zoom-controls button:focus-visible,
.band-mark:focus-visible {
  outline: 2px solid var(--vp-c-brand-1);
  outline-offset: 2px;
}

.spectral-chart {
  display: block;
  width: 100%;
  min-width: 860px;
  height: auto;
  font-family: var(--vp-font-family-base);
  cursor: crosshair;
  touch-action: pan-y;
  user-select: none;
}

.chart-grid line {
  stroke: var(--vp-c-divider);
  stroke-width: 1;
  stroke-dasharray: 3 6;
}

.chart-grid text {
  fill: var(--vp-c-text-3);
  font-size: 11px;
  font-weight: 650;
}

.axis-label {
  fill: var(--vp-c-text-2);
  font-size: 12px;
  font-weight: 750;
}

.axis-line {
  stroke: var(--vp-c-text-2);
  stroke-width: 1.25;
}

.row-divider {
  stroke: var(--vp-c-divider);
  stroke-width: 1;
}

.instrument-label {
  fill: var(--vp-c-text-1);
  font-size: 14px;
  font-weight: 760;
}

.instrument-detail {
  fill: var(--vp-c-text-3);
  font-size: 11px;
}

.current-row {
  fill: color-mix(in srgb, var(--vp-c-brand-1) 4%, transparent);
  stroke: var(--vp-c-brand-1);
  stroke-width: 2;
}

.band-mark {
  cursor: help;
}

.band-mark rect {
  stroke: color-mix(in srgb, var(--vp-c-text-1) 28%, transparent);
  stroke-width: 1;
  opacity: 0.78;
  transition: opacity 0.15s ease, stroke-width 0.15s ease;
}

.band-mark rect.is-current {
  opacity: 1;
  stroke: var(--vp-c-text-1);
  stroke-width: 1.5;
}

.band-mark:hover rect,
.band-mark:focus rect {
  opacity: 1;
  stroke: var(--vp-c-text-1);
  stroke-width: 2;
}

.band-tooltip rect {
  fill: var(--vp-c-bg);
  stroke: var(--vp-c-divider);
  stroke-width: 1;
}

.band-tooltip text {
  fill: var(--vp-c-text-1);
  font-size: 11px;
  font-weight: 750;
}

.band-tooltip .tooltip-range {
  fill: var(--vp-c-text-3);
  font-size: 10px;
  font-weight: 600;
}

.zoom-selection {
  fill: color-mix(in srgb, var(--vp-c-brand-1) 20%, transparent);
  stroke: var(--vp-c-brand-1);
  stroke-width: 1.5;
  stroke-dasharray: 5 4;
}

.response-instrument path {
  stroke-width: 1.7;
  stroke-linecap: round;
  stroke-linejoin: round;
  opacity: 0.72;
  vector-effect: non-scaling-stroke;
}

.response-instrument path.is-current {
  stroke-width: 3.4;
  opacity: 1;
}

.band-annotation {
  stroke: var(--vp-c-bg);
  stroke-width: 3px;
  paint-order: stroke fill;
  font-size: 9px;
  font-weight: 680;
}

.band-annotation.is-current {
  font-size: 10px;
  font-weight: 850;
}

.availability-note,
.empty-state {
  margin: 0.75rem 0 0;
  color: var(--vp-c-text-2);
  font-size: 0.82rem;
}

.instrument-legend {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.45rem 0.8rem;
  margin-top: 0.9rem;
  color: var(--vp-c-text-2);
  font-size: 0.75rem;
}

.instrument-legend strong {
  color: var(--vp-c-text-1);
  font-size: 0.72rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.instrument-legend span {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.instrument-legend i {
  width: 1.4rem;
  height: 0.65rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 3px;
}

.comparison-note {
  margin: 0.75rem 0 0;
  color: var(--vp-c-text-3);
  font-size: 0.75rem;
}

@media (max-width: 760px) {
  .spectral-comparison {
    padding: 0.85rem;
  }

  .comparison-heading {
    display: grid;
    align-items: stretch;
  }

  .view-switch {
    justify-self: start;
  }

  .zoom-controls {
    grid-template-columns: 1fr 1fr;
  }

  .zoom-label,
  .zoom-readout {
    grid-column: 1 / -1;
  }
}

@media (prefers-reduced-motion: reduce) {
  .current-row,
  .response-instrument path.is-current {
    filter: none;
  }

  .band-mark rect {
    transition: none;
  }
}
</style>
