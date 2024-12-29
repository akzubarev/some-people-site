<template>
  <div class="flex relative w-full gap-1" :class="horizontal ? 'flex-row' : 'flex-col'">
    <div v-if="!!title" class="flex flex-col md:flex-row justify-between">
      <label class="text-xl"> {{ title }} </label>
      <slot name="label"/>
    </div>
    <div class="flex flex-col w-full items-end gap-1">
      <slot name="content"/>
      <div class="flex relative w-full items-end gap-1">
        <Field
            class="form-input" :autocomplete="autocomplete ? 'on' : 'off'"
            :type="passVisible ? 'text' : type" :name="name" v-model="result"
            :placeholder="placeholder" @change="$emit('input', name, result, true)"
        />
        <inline-svg
            v-if="type=='password'" @click="passVisible = !passVisible"
            class="absolute right-2 bottom-3 text-3xl text-gray-400"
            :src="require(`@/assets/images/icons/auth/eye${passVisible ? '-off' : ''}.svg`)"
        />
      </div>
      <div v-if="errors" class="text-sm font-semibold">{{ errors }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {Field} from "vee-validate";
import {ref} from "vue";

const passVisible = ref(false)
const props = defineProps({
  'title': {type: String},
  'name': {type: String},
  'placeholder': {type: String},
  'errors': {type: String},
  'horizontal': {type: Boolean, default: true},
  'autocomplete': {type: Boolean, default: false},
  'type': {type: String, default: 'text'},
  'defaultValue': {},
})
const result = ref(props.defaultValue)
defineEmits(['input'])
</script>