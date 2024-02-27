<template>
  <div class="flex flex-col items-center justify-center gap-6 h-full min-h-[300px] px-12">
    <inline-svg
        :src="require('@/assets/images/icons/matrix/Lock.svg')"
        width="70" height="70"
        class="max-w-none text-gray-400"
    />
    <span class="text-3xl lg:text-4xl text-center">{{$t('common.comingSoonTitle')}}</span>
    <span class="text-xl lg:text-2xl text-center text-gray-400">{{$t('common.comingSoonDescription')}}</span>
  </div>
</template>


<script setup>
</script>
