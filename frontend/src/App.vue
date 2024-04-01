<template>
  <teleport to="head title">{{ pageTitle }}</teleport>
  <teleport to="head">
    <meta
        :name="name"
        :content="content"
        v-for="(content, name) in metaData"
        :key="name"
    />
  </teleport>
  <teleport to="body">
    <div v-if="$store.getters['body/actionLoader']" class="ActionLoader">
      <SpinLoder/>
    </div>
  </teleport>
  <PullToRefresh scroll-root="true" @refresh="refresh">
    <router-view/>
  </PullToRefresh>
  <!-- <Glares/> -->
</template>
<style>


:root {
  /* IMPORTANT!: Добавление новых цветов необходимо обсуждать */

  --accent-color-start: #56405f;
  --accent-color-end: #44405f;
  --bg-card: #404B5F;

  /* dark colors */
  --dark-primary-color: #101214; /* Основной темный цвет сайта */
  --dark-secondary-color: #181B1F; /* Второстепенный темный цвет */
  --dark-accent-color: #310533; /* Акцентный темный цвет */
  --dark-text-color: #DADFE5; /* Основной цвет текста в темной теме */
  --dark-text-secondary-color: #8A9099; /* Второстепенный цвет текста в темной теме */
  --dark-link-color: #5c159a; /* Цвет ссылок в темной теме */
}
</style>
<style lang="scss">
// @import "~bootstrap-icons/font/bootstrap-icons.css";
// @import "~apexcharts/dist/apexcharts.css";
// @import "~quill/dist/quill.snow.css";
// @import "~animate.css";
// @import "~nouislider/distribute/nouislider.css";
// @import "~@fortawesome/fontawesome-free/css/all.min.css";
// @import "~socicon/css/socicon.css";
// @import "~line-awesome/dist/line-awesome/css/line-awesome.css";
// @import "~@yaireo/tagify/src/tagify.scss";
// @import "~dropzone/dist/dropzone.css";
// @import "~@vueform/multiselect/themes/default.css";
// @import "~prism-themes/themes/prism-shades-of-purple.css";
// @import "~element-plus/lib/theme-chalk/index.css";

// Main demo style scss
// @import "assets/sass_14/plugins";
@import "assets/sass/style";
// @import "assets/sass/plugins.dark";
// @import "assets/sass/style.dark";


@media (max-width: 479px) {
  #crisp-chatbox > div > a {
    display: none !important;
  }
}

.ActionLoader {
  position: fixed;
  top: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.6);
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

input:-webkit-autofill {
  background: var(--kt-input-solid-bg) !important;
}

.swal2-popup {
  background: #13161A !important;
  border-radius: 1rem !important;
  color: white i !important;
}

.swal2-icon {
  border: 0 !important;
}

.swal2-popup {
  background: theme('colors.gray.900');
  border-radius: theme('borderRadius.2xl');
  color: white;
}

.swal2-actions {
  margin-top: 20px !important;
}

.swal2-backdrop-show {
  background: rgba(0, 0, 0, 0.75) !important;
}

.swal2-close:focus {
  box-shadow: unset !important;
}

.form-check-input {
  margin-left: 0 !important
}

.form-check {
  padding: 0
}

// @media (min-width: 620px) {
//   body {
//     font-family: "Suisse Regular";
//   }
//  }
html,
body,
#app {
  overflow: hidden;
  height: 100%;
}

.card {
  border-radius: theme('borderRadius.2xl');
  background: theme('colors.gray.700');

  .card-title {
    font-size: theme('fontSize.2xl');
  }

  .card-header, .card-body {
    padding: theme('spacing.6');
  }

  // .card-header:has(+ .card-body) {
  //   padding-bottom: theme('spacing.3')
  // }
  .card-header + .card-body {
    padding-top: 0
  }
}

.text-accent {
  background: linear-gradient(45deg, theme('colors.accent.green') 0%, theme('colors.accent.emerald') 50%, theme('colors.accent.blue') 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.Layout-Body {
  margin: auto
}
</style>
<style>
@tailwind base;
@tailwind components;
@tailwind utilities;
</style>
<script setup lang="ts">
import {defineComponent, onMounted, ref} from "vue"
import ActionModal from "@/components/action-modal/ActionModal.vue";
// import { Mutations } from "@/store/enums/StoreEnums"
import {pageTitle, metaData} from "./store"
import SpinLoder from "@/components/SpinLoader.vue"
import PullToRefresh from "@/components/PullToRefresh.vue"
import Popup from "@/components/Popup"

const refresh = () => {
  window.location.reload()
}

const showSpecialOffer = ref(false)
const changeDomain = () => {
  window.location = "http://residual.community";
}
// const changeHost = !['residual.community', 'localhost', '127.0.0.1'].includes(window.location.hostname)
</script>
