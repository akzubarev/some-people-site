<template>
  <div
      class="w-full m-auto min-h-screen h-full relative bg-[#404B5F]
      flex flex-center flex-col flex-col-fluid items-center justify-center">
    <img
        class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 h-[100%] opacity-40 z-0"
        :src="require('@/assets/images/logos/moth.svg')"/>
    <div
        class="lg:w-1/2 w-full p-6 mx-auto rounded-2xl bg-gray-700 bg-opacity-60 absolute z-10 gap-3">
      <div class="text-2xl text-center">Авторизация</div>
      <router-view/>
      <ul
          class="nav nav-stretch nav-line-tabs nav-line-tabs-2x
              border-transparent !flex-nowrap hide-scrollbar justify-center
              overflow-y-hidden overflow-x-auto !h-wrap"
      >
        <li class="nav-item my-0 py-0" v-if="$route.path.includes('sign-up')">
          <router-link
              to="/sign-in" active-class="active"
              class="text-lg nav-link text-active-primary me-6 active"
          >
            <!--                  $route.path.includes('sign-in') && 'active']"-->
            {{ $t("auth.signIn") }}
          </router-link>
        </li>
        <li class="nav-item my-0 py-0" v-if="$route.path.includes('sign-in')">
          <router-link
              to="/sign-up" active-class="active"
              class="text-lg nav-link text-active-primary me-6 active"
          >
            <!--                  $route.path.includes('sign-up') && 'active']"-->
            {{ $t("auth.signUp") }}
          </router-link>
        </li>
      </ul>
      <!--            <div class="flex flex-col justify-between items-center gap-1 mt-6">-->
      <!--              <div v-for="item in links" :key="item"-->
      <!--                   @click="openLink(item.url)" class="cursor-pointer">-->
      <!--              <span class="text-md text-gray-400 underline">-->
      <!--                {{ item.title }}-->
      <!--              </span>-->
      <!--              </div>-->
      <!--            </div>-->
    </div>
  </div>
</template>
<script setup lang="ts">
import {useI18n} from "vue-i18n";

const {t} = useI18n()

const links = [
  {
    title: t('promo.privacyPolicy'),
    url: t('promo.privacyPolicyLink'),
  },
  {
    title: t('promo.termsOfAgreement'),
    url: t('promo.termsOfAgreementLink'),
  },
]

const openLink = link => {
  const w = window.open(link, "_blank")
  w.focus()
}
</script>
