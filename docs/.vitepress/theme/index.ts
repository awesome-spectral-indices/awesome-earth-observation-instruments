import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import InstrumentIndex from './components/InstrumentIndex.vue'
import InstrumentSection from './components/InstrumentSection.vue'
import InstrumentTabs from './components/InstrumentTabs.vue'
import InstrumentTimeline from './components/InstrumentTimeline.vue'
import './styles.css'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('InstrumentIndex', InstrumentIndex)
    app.component('InstrumentSection', InstrumentSection)
    app.component('InstrumentTabs', InstrumentTabs)
    app.component('InstrumentTimeline', InstrumentTimeline)
  }
} satisfies Theme
