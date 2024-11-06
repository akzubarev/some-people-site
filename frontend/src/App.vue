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
@tailwind base;
:root {
  --content-primary: 220 220 220;
  --content-secondary: 55 60 60;
  --content-secondary-shadowed: 98 106 106;
  --content-disabled: 140 140 140;
  --content-muted: 60 60 60;
  --content-accent: 207 207 207;

  --bg-default: 64 75 95;
  --bg-shadowed: 29 33 38;

  --gradient-start: 88 64 95;
  --gradient-end: 68 64 95;
}

@layer base {
  @font-face {
    font-family: 'Montserrat';
    font-style: normal;
    font-weight: 400;
    font-display: swap;
    src: url(https://fonts.googleapis.com/) format('woff2');
  }
}

div {
  @apply font-primary text-content-primary;
}

@tailwind components;

.btn {
  @apply flex justify-center items-center p-3 rounded-xl;
}

.btn-gradient {
  @apply btn bg-gradient-to-r from-gradient-start to-gradient-end;
}

.btn-gray {
  @apply btn bg-gray-800;
}

.btn-white {
  @apply btn bg-white hover:bg-gray-500;
}

.btn-outline {
  @apply btn bg-transparent border border-[1px] border-content-primary;
}

.form-input {
  @apply flex flex-row items-center w-full basis-full lg:basis-2/3 p-3 mt-2 lg:mt-0 bg-bg-primary rounded-xl;
}

.Layout-Body {
  margin: auto
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

.arrow {
  @apply text-xs transition-transform ease-linear rotate-0;
  color: var(--content-primary);
  width: 20px;
  height: 20px;

}

.arrow_expanded {
  @apply rotate-180;
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

@tailwind utilities;
/* Hide scrollbar for Chrome, Safari and Opera */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.no-scrollbar {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}

#app {
  overflow: hidden;
  height: 100%;
}

</style>

<script setup lang="ts">
import {pageTitle, metaData} from "./store"
import SpinLoder from "@/components/SpinLoader.vue"
import PullToRefresh from "@/components/PullToRefresh.vue"

const refresh = () => {
  window.location.reload()
}

</script>
