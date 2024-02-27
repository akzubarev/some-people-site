import LayoutConfigTypes from "@/core/config/LayoutConfigTypes"

const config: LayoutConfigTypes = {
  layoutnum: 14,
  main: {
    type: "default",
    primaryColor: "#009EF7",
    logo: {
      dark: "media/logos/logo-1.svg",
      light: "media/logos/logo-1-dark.svg"
    }
  },
  loader: {
    logo: "media/logos/logo-1-dark.svg",
    display: true,
    type: "neon-bullet"
  },
  scrollTop: {
    display: true
  },
  header: {
    display: true,
    menuIcon: "font",
    // "theme": "dark",
    theme: "dark",
    width: "fixed",
    fixed: {
      desktop: true,
      tabletAndMobile: false
    }
  },
  toolbar: {
    display: false,
    width: "fixed",
    fixed: {
      desktop: true,
      tabletAndMobile: true
    }
  },
  aside: {
    display: true,
    theme: "light",
    fixed: true,
    menuIcon: "svg",
    minimized: false,
    minimize: false,
    hoverable: false,
    toggle: false
  },
  content: {
    width: "fixed"
  },
  footer: {
    width: "fluid"
  }
}

export default config
