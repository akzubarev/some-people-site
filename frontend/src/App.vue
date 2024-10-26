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
@tailwind components;
@tailwind utilities;

:root {
  --text-default: 218 223 229;
  --text-disabled: 138 144 153;
  --text-accent: 92 21 154;

  --bg-default: 64 75 95;
  --bg-shadowed: 29 33 38;

  --gradient-start: 88 64 95;
  --gradient-end: 68 64 95;
}

.btn {
  background: linear-gradient(85deg, rgb(var(--gradient-start)), rgb(var(--gradient-end)));
  background-clip: text;
  color: transparent;

  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  z-index: 0;
  text-decoration: none;

  &::before {
    content: "";
    position: absolute;
    z-index: -1;
    inset: 0;
    border: 1px solid transparent;
    border-radius: 10px;
    background: inherit;
    background-origin: border-box;
    background-clip: border-box;
    //-webkit-mask: linear-gradient(#fff 0 0) padding-box,
    //linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    -webkit-mask-repeat: no-repeat;
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

.Layout-Body {
  margin: auto
}
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
