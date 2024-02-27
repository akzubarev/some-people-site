<template>
  <div class="grid gap-4 grid-cols-1 lg:grid-cols-2">
    <div class="card relative flex justify-between p-6 items-center">
      <div class="flex flex-col gap-2 h-full">
        <div class="text-4xl h-full"> {{ $t('main.activitiesTitle') }}</div>
        <div class="" :class="$style.social_network">
          <a :href="$t('main.activitiesLink')"
             class="btn btn-outline btn-outline-primary">
            {{ $t("common.actions.go") }}
          </a>
        </div>
      </div>
      <inline-svg
          src="require('@/assets/images/icons/dashboard/telegram.svg')"
      />
    </div>
  </div>
  <span class="text-2xl">{{ $t('common.products') }}</span>
</template>

<script setup lang="ts">

</script>


<style module lang="scss">
.social_network {
  @apply bg-transparent #{!important};
}

;
</style>
