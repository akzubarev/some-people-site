<template>
  <div class="flex relative w-full gap-1" :class="horizontal ? 'flex-row' : 'flex-col'">
    <label class="flex items-center basis-full lg:basis-1/3 text-xl"> {{ title }} </label>
    <slot/>
     <inline-svg
          v-if="type=='password'" @click="passVisible = !passVisible"
          class="absolute right-1 bottom-1 text-3xl text-gray-400"
          :src="require(`@/assets/images/icons/auth/eye${passVisible ? '-off' : ''}.svg`)"
      />
    <Field
        class="form-input" :autocomplete="autocomplete ? 'on' : 'off'"
        :type="passVisible ? 'text' : type" :name="name" v-model="props.v_model"
        :placeholder="placeholder"
    />
    <div v-if="errors" class="input-error-message">{{ errors }}</div>
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
  'v_model': {type: String},
})
</script>