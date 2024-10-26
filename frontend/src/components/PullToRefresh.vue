<template>
	<div class="PullToRefresh" ref="element">
		<div class="PullToRefresh-Progress" :style="{width: `${progress}%`}"></div>
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
<style lang="scss">
.PullToRefresh {
	overflow-y: auto;
	max-height: 100%;
	&-Progress {
		background: linear-gradient(85deg, var(--gradient-start), var(--gradient-end));
		height: 2px;
		position: absolute;
	}
}
</style>