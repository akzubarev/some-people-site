<template>
  <div class="Avatar" :style="[style, customStyle]" aria-hidden="true">
    <img
        v-if="showFlag && country"
        class="rounded-full object-cover absolute -right-[3px] top-[1px] z-10 !border-[2px] border-black aspect-square"
        :class="`min-w-[${this.size * 0.4}px] max-w-[${this.size * 0.4}px] min-h-[${this.size * 0.4}px] max-h-[${this.size * 0.4}px]`"
        :src="`https://flagcdn.com/h40/${country.toLowerCase()}.png`"
    />
    <div class="Avatar-Wrapper rounded-full">
      <img
          v-if="this.isImage"
          class="Avatar-Image"
          :src="this.src"
          @error="onImgError"
      />
      <span v-show="!this.isImage" style="line-height: 1rem">{{
          userInitial
        }}</span>
      <div v-show="this.icon" v-html="this.icon" style="scale: 1.5"/>
    </div>
  </div>
</template>
<style lang="scss">
.Avatar {
  position: relative;
  width: 100%;
  // border: 1px solid #673ab7;

  &-Wrapper {
    overflow: auto;
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    // font-size: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &-Pixel {
    width: 100%;
  }

  &-Image {
    width: 100%;
  }
}
</style>
<script>
const getInitials = username => {
  if (!String(username).includes(" ")) {
    return username
  }
  const parts = username.split(/[ -]/)
  let initials = ""

  for (let i = 0; i < parts.length; i++) {
    initials += parts[i].charAt(0)
  }

  if (initials.length > 3 && initials.search(/[A-Z]/) !== -1) {
    initials = initials.replace(/[a-z]+/g, "")
  }

  initials = initials.substr(0, 2).toUpperCase()

  return initials
}

export default {
  name: "avatar",
  props: {
    username: {
      type: String
    },
    initials: {
      type: String
    },
    backgroundColor: {
      type: String
    },
    color: {
      type: String
    },
    customStyle: {
      type: Object
    },
    inline: {
      type: Boolean
    },
    size: {
      type: Number,
      default: null
    },
    src: {
      type: String
    },
    rounded: {
      type: Boolean,
      default: true
    },
    lighten: {
      type: Number,
      default: 80
    },
    parser: {
      type: Function,
      default: getInitials,
      validator: parser => typeof parser("John", getInitials) === "string"
    },
    icon: {
      type: String,
      default: ""
    },
    showFlag: {
      type: Boolean,
      default: false
    },
    country: {
      type: String,
      default: "World"
    }
  },

  data() {
    return {
      backgroundColors: [
        // "#F44336",
        // "#FF4081",
        // "#9C27B0",
        // "#673AB7",
        // "#3F51B5",
        // "#2196F3",
        // "#03A9F4",
        // "#00BCD4",
        // "#009688",
        // "#4CAF50",
        // "#8BC34A",
        // "#CDDC39",
        // /* '#FFEB3B' , */ "#FFC107",
        // "#FF9800",
        // "#FF5722",
        // "#795548",
        // "#9E9E9E",
        // "#607D8B"
        "#FF7C0233",
        "#CB1D7B33",
        "#FF980033",
        "#FF572233",
        "#79554833",
        "#9E9E9E33",
        "#607D8B33",
        "#F4433633",
        "#FF408133",
        "#9C27B033",
        "#673AB733",
        "#3F51B533",
        "#03A9F433",
        "#00BCD433",
        "#00968833",
        "#4CAF5033",
        "#8BC34A33",
        "#CDDC3933"
      ],
      imgError: false
    }
  },

  mounted() {
    if (!this.isImage) {
      this.$emit("avatar-initials", this.username, this.userInitial)
    }
  },

  computed: {
    background() {
      if (!this.isImage) {
        return (
            this.backgroundColor ||
            this.randomBackgroundColor(
                this.username.length,
                this.backgroundColors
            )
        )
      }
      return undefined
    },

    fontColor() {
      if (!this.isImage) {
        return this.color || this.lightenColor(this.background, this.lighten)
      }
      return undefined
    },

    isImage() {
      return !this.imgError && Boolean(this.src)
    },

    style() {
      const style = {
        display: this.inline ? "inline-flex" : "flex",
        width: (this.size && `${this.size}px`) || null,
        height: (this.size && `${this.size}px`) || null,
        borderRadius: this.rounded ? "50%" : 0,
        lineHeight:
            (this.size && `${this.size + Math.floor(this.size / 20)}px`) || null,
        fontWeight: "bold",
        fontSize: `${Math.floor(this.size / 2) || 22}px`,
        alignItems: "center",
        justifyContent: "center",
        textAlign: "center",
        userSelect: "none"
      }

      const imgBackgroundAndFontStyle = {
        background: `transparent url('${this.src}') no-repeat scroll 0% 0% / ${this.size}px ${this.size}px content-box border-box`
      }

      const initialBackgroundAndFontStyle = {
        backgroundColor:
            this.background === "#3150f6" ? "#1a5635" : this.background,
        font: `${Math.floor(this.size / 2.5)}px/${Math.floor(
            this.size / 1
        )}px `, //Helvetica, Arial, sans-serif
        // color: this.fontColor
        color: this.color || "#fff"
      }

      const backgroundAndFontStyle = this.isImage
          ? imgBackgroundAndFontStyle
          : initialBackgroundAndFontStyle

      Object.assign(style, backgroundAndFontStyle)

      return style
    },

    userInitial() {
      if (!this.isImage) {
        const initials =
            this.initials || this.parser(this.username, getInitials)
        return initials
      }
      return ""
    }
  },

  methods: {
    initial: getInitials,

    onImgError() {
      this.imgError = true
    },

    randomBackgroundColor(seed, colors) {
      return colors[seed % colors.length]
    },

    lightenColor(hex, amt) {
      // From https://css-tricks.com/snippets/javascript/lighten-darken-color/
      let usePound = false

      if (hex[0] === "#") {
        hex = hex.slice(1)
        usePound = true
      }

      const num = parseInt(hex, 16)
      let r = (num >> 16) + amt

      if (r > 255) r = 255
      else if (r < 0) r = 0

      let b = ((num >> 8) & 0x00ff) + amt

      if (b > 255) b = 255
      else if (b < 0) b = 0

      let g = (num & 0x0000ff) + amt

      if (g > 255) g = 255
      else if (g < 0) g = 0

      return (usePound ? "#" : "") + (g | (b << 8) | (r << 16)).toString(16)
    }
  }
}
</script>
