<template>
  <teleport to="head title">{{ pageTitle }}</teleport>
  <teleport to="head">
    <meta v-for="(content, name) in metaData" :name="name" :content="content" :key="name"/>
  </teleport>
  <teleport to="body">
    <div v-if="$store.getters['body/actionLoader']" class="ActionLoader">
      <SpinLoder/>
    </div>
  </teleport>
  <PullToRefresh scroll-root="true" @refresh="refresh">
    <router-view/>
  </PullToRefresh>
</template>
<style>


:root {
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

@import "assets/sass/style";

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
// import ActionModal from "@/components/ActionModal.vue";
import {pageTitle, metaData} from "./store"
import SpinLoder from "@/components/SpinLoader.vue"
import PullToRefresh from "@/components/PullToRefresh.vue"
// import Popup from "@/components/Popup"

const refresh = () => {
  window.location.reload()
}

</script>
