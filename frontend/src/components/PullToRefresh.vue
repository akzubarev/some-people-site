<template>
	<div class="h-full overflow-hidden no-scrollbar" ref="element">
		<div class="absolute h-2 rounded-xl bg-gradient-to-r from-gradient-start to-gradient-end" :style="{width: `${progress}%`}"></div>
		<slot/>
	</div>
</template>
<script setup>
import { ref, onMounted, computed } from 'vue'
const element = ref()
const scrollTop = ref(0)
const convert = 1.5
const emit = defineEmits(['refresh'])
onMounted(() => {
	element.value.addEventListener('scroll', e=>{
		scrollTop.value = e.target.scrollTop
		if (scrollTop.value < -100*convert) {
			emit('refresh')
		}
	})
})
const progress = computed(() => {
	if (scrollTop.value < 0) {
		return Math.min(-scrollTop.value/convert, 100)
	}
	return 0
})
</script>