<template>
  <Modal :hide-x="hideX" @close="$emit('close')">
    <div class="flex flex-col w-full gap-6 items-center p-12">
      <slot name="icon">
        <img :src="typeConf[type || defaultConf].icon" class=""/>
      </slot>

      <slot name="body">
        <span v-if="title" class="text-3xl text-center">
          {{ title }}
        </span>
        <span v-if="description" class="text-xl text-center text-gray-400">
          {{ description || typeConf[type || defaultConf].defaultText }}
        </span>
      </slot>
      <slot name="button">
        <button
            class="btn-primary min-w-[20%] h-fit w-full md:w-fit"
            v-if="!(hideButton !== undefined && hideButton == true)"
            @click="$emit('submit')">
          {{ buttonText || typeConf[type || defaultConf].buttonText }}
        </button>
      </slot>
    </div>
  </Modal>
</template>


<script setup>
import Modal from '@/components/Modal.vue'


const props = defineProps(['type', 'title', 'description', 'hideButton', 'buttonStyle', 'buttonText', 'hideX'])
const emit = defineEmits(['submit'])

const typeConf = {
  lock: {
    icon: require('@/assets/images/icons/common/lock-gradient.svg'),
    defaultText: 'Раздел в разработке',
    buttonText: 'Ok',
  },
}
const defaultConf = 'lock'
</script>
