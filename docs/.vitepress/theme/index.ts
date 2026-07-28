import { defineComponent, h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import { useData, type Theme } from 'vitepress'
import InstrumentHeroIdentity from './components/InstrumentHeroIdentity.vue'
import InstrumentIndex from './components/InstrumentIndex.vue'
import InstrumentSection from './components/InstrumentSection.vue'
import InstrumentTabs from './components/InstrumentTabs.vue'
import InstrumentTimeline from './components/InstrumentTimeline.vue'
import LandingActions from './components/LandingActions.vue'
import SpectralComparison from './components/SpectralComparison.vue'
import './styles.css'
import './custom.css'

const Layout = defineComponent({
  name: 'AeoiLayout',
  setup() {
    const { frontmatter } = useData()

    return () =>
      h(DefaultTheme.Layout, null, {
        'home-hero-actions-after': () => {
          const instrumentId = frontmatter.value.instrumentId
          return typeof instrumentId === 'string'
            ? h(InstrumentHeroIdentity, { instrumentId })
            : null
        }
      })
  }
})

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    app.component('InstrumentIndex', InstrumentIndex)
    app.component('InstrumentSection', InstrumentSection)
    app.component('InstrumentTabs', InstrumentTabs)
    app.component('InstrumentTimeline', InstrumentTimeline)
    app.component('LandingActions', LandingActions)
    app.component('SpectralComparison', SpectralComparison)
  }
} satisfies Theme
