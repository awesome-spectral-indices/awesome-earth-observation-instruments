import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import InstrumentIndex from './components/InstrumentIndex.vue'
import InstrumentSection from './components/InstrumentSection.vue'
import InstrumentTabs from './components/InstrumentTabs.vue'
import './styles.css'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('InstrumentIndex', InstrumentIndex)
    app.component('InstrumentSection', InstrumentSection)
    app.component('InstrumentTabs', InstrumentTabs)
  }
} satisfies Theme
