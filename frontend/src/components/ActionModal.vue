<template>
  <Popup :hide-x="hideX" @close="$emit('close')">
    <div class="flex flex-col w-full gap-6 items-center p-12">
      <slot name="icon">
        <img :src="typeConf[type || defaultConf].icon" class=""/>
      </slot>

      <slot name="body">
        <span v-if="title" class="text-3xl text-center">
          {{ title }}
        </span>
        <span v-if="description" class="text-xl text-center text-gray-400">
          {{ description }}
        </span>
      </slot>
      <slot name="button">
        <button
            class="btn h-fit w-full md:w-fit"
            v-if="!(hideButton !== undefined && hideButton == true)"
            @click="$emit('submit')">
          {{ buttonText || typeConf[type || defaultConf].buttonText }}
        </button>
      </slot>
    </div>
  </Popup>
</template>


<script setup>
import Popup from '@/components/Popup.vue'
import {useI18n} from 'vue-i18n'

const {t} = useI18n()

const props = defineProps(['type', 'title', 'description', 'hideButton', 'buttonStyle', 'buttonText', 'hideX'])
const emit = defineEmits(['submit'])

const typeConf = {
  success: {
    icon: require('@/assets/images/icons/action-modal/success.svg'),
    buttonText: 'Ok',
  },
  info: {
    icon: require('@/assets/images/icons/action-modal/info.svg'),
    buttonText: t('common.actions.continue'),
  },
  smile: {
    icon: require('@/assets/images/icons/action-modal/smile-happy.svg'),
    buttonText: t('common.actions.continue'),
  },
  sad: {
    icon: require('@/assets/images/icons/action-modal/smile-sad.svg'),
    buttonText: t('common.actions.continue'),
  },
  alert: {
    icon: require('@/assets/images/icons/action-modal/alert.svg'),
    buttonText: t('common.actions.continue'),
  },
  lock: {
    icon: require('@/assets/images/icons/common/lock-gradient.svg'),
    buttonText: 'Ok',
  },
  developing: {
    icon: require('@/assets/images/icons/action-modal/developing.svg'),
    buttonText: 'Ok',
  },
}
const defaultConf = 'success'
</script>
