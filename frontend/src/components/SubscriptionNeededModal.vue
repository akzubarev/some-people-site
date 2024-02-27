<template>
  <Popup @close="$emit('close')">
    <div class="flex flex-col p-16 gap-8 items-center justify-center">
      <div
        class="p-4 rounded-full w-fit"
        :style="`background: linear-gradient(85deg,var(--accent-color-start),var(--accent-color-end)) !important`"
        >
        <inline-svg
          height="30"
          width="30"
          :src="require('@/assets/images/icons/matrix/Lock.svg')"
        ></inline-svg>
      </div>
      <span class="text-4xl text-center">{{ $t('subscription.subscriptionNeededTitle') }}</span>
      <span class="text-center text-gray-400">{{ $t('subscription.calltosubscribebotttom') }}</span>
      <button class="btn btn-accent w-full md:w-fit text-white" @click="$router.push('/subscription')">
        {{ $t('subscription.subscribe') }}
      </button>
    </div>
  </Popup>
</template>


<script setup>
import Popup from '@/components/Popup'
</script>
