<template>
  <div class="flex flex-col" :class="depthExpanded ? 'gap-3' : ''">
    <div
        @click="() => (depthExpanded = !depthExpanded)"
        class="flex justify-between items-center cursor-pointer pe-2"
    >
      <!--      <h2 :class="s.filter_title">{{ $t("matrix.tree.depth") }}</h2>-->
      <h2 class="form-check-label text-primary cursor-pointer">
        {{ $t("matrix.tree.depth") }}
      </h2>
      <inline-svg
          :class="[s.arrow, { [s.arrow_expanded]: depthExpanded }]"
          :src="require('@/assets/images/icons/chevrone.svg')"
      />
    </div>
    <div :class="depthExpanded ? 'h-wrap' : 'h-0'"
         class="flex flex-col justify-center gap-4 transition-all
       overflow-hidden duration-300"
    >
      <div class="flex gap-2 flex-wrap">
        <div
            v-for="i in 21" :key="i" role="button"
            @click="depth=i; $emit('change', depth)"
            :class="[
								'flex justify-center items-center rounded-lg w-[42px] h-[42px]',
								i==depth&&'bg-accent-green text-black'||'bg-gray-800'
							]"
        >
          <span>{{ i }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

import s from "./styles.module.scss"
import {ref} from "vue";

const props = defineProps(['depth'])
const emit = defineEmits(['change'])

const depthExpanded = ref(false)
const depth = ref(props.depth)
</script>
