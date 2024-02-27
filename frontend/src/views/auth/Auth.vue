<template>
  <div class="flex flex-col AuthLayout">
    <div class="flex flex-center flex-col flex-col-fluid p-3 pb-lg-20">
      <div class="AuthLayout-Content w-full flex justify-center flex-col">
        <div class="p-6 lg:w-[500px] w-full m-auto">
          <inline-svg
              :src="require('@/assets/images/logos/frostpunk.jpg')"/>
        </div>
        <div class="lg:w-[500px] w-full p-6 mx-auto card">
          <ul
              class="nav nav-stretch nav-line-tabs nav-line-tabs-2x
              border-transparent !flex-nowrap hide-scrollbar justify-center
              overflow-y-hidden overflow-x-auto"
          >
            <li class="nav-item">
              <router-link
                  to="/sign-in" active-class="active"
                  :class="['text-2xl nav-link text-active-primary me-6',
                  $route.path.includes('sign-in') && 'active']"
              >
                {{ $t("auth.signIn") }}
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                  to="/sign-up" active-class="active"
                  :class="['text-2xl nav-link text-active-primary me-6',
                  $route.path.includes('sign-up') && 'active']"
              >
                {{ $t("auth.signUp") }}
              </router-link>
            </li>
          </ul>
          <router-view/>
          <div class="flex flex-col justify-between items-center gap-1 mt-6">
            <div v-for="item in links" :key="item"
                 @click="openLink(item.url)" class="cursor-pointer">
              <span class="text-md text-gray-400 underline">
                {{ item.title }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style lang="sass">
.AuthLayout

  &-Content
    position: relative
    z-index: 2

  &-Lang
    @apply m-6
    margin-left: auto
</style>
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
