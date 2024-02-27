<template>
  <div
    class="flex flex-col gap-8 items-center text-white mx-auto w-full md:max-w-[600px] p-4 mt-6 text-center">
    <inline-svg
      :src="require('@/assets/images/icons/matrix/Info.svg')"
      style="color: var(--kt-primary);"
      height="3em"
      width="3em"
      />
      <span class=" fs-2">
        {{ $t("auth.registrationSuccess") }}
      </span>
      <span class="whitespace-pre-wrap">{{ $t("auth.pleaseActivateEmail") }}</span>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "vue"

export default defineComponent({
  name: "confirm",
  components: {}
})
</script>
