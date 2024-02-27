<template>
	<div class="flex flex-col gap-1 cursor-pointer">
		<div
			@click="toggleExpand"
			class="flex justify-between items-center py-1 ps-2"
			:class="{'bg-gray-800 rounded-2xl': isSelected}">

			<slot v-bind="{target, depth, childrensCount, isExpanded, isSelected}" ></slot>

			<div class="flex justify-end h-100 items-center me-2 cursor-pointer">
				<inline-svg
				v-if="childrensCount"
				class="w-[16px] h-[16px] text-[--dark-text-color] transition-all -rotate-90 text-white"
				:class="[ isExpanded && 'rotate-0']"
				:src="require('@/assets/images/icons/chevrone.svg')"
				/>
			</div>
		</div>

		<div v-if="loading" class="flex w-full justify-center">
			<SpinLoader class="max-h-[3rem]"/>
		</div>

		<div v-else-if="isExpanded" class="flex flex-col gap-1" :class="{'ms-3': depth > 0}">

			<template v-for="{children, count}, i in childrens" :key="i">
				<RecursiveList
					:target="children"
					:depth="depth + 1"
					:get-childrens="getChildrens"
					:childrens-count="count"
					:is-selected-check="isSelectedCheck"
					@select="emitSelect">
					<template #default="props">
						<slot v-bind="props" ></slot>
					</template>
				</RecursiveList>
			</template>

			<div class="flex justify-center mt-2" v-if="childrensCount > 50">
				<pagination
					v-model="page"
					:options="{
						theme: 'bootstrap4',
						texts: {
							count: ''
						}
					}"
					:records="childrensCount"
					:per-page="50"
					@paginate="onPaginate"/>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'RecursiveList',
}
</script>

<script setup>
import { ref, onMounted, computed } from "vue"
import SpinLoader from '@/components/SpinLoader.vue'
import Pagination from "v-pagination-3"


const props = defineProps({
	target: {},
	depth: { default: 0 },
	childrensCount: { default: 0 },
	getChildrens: {},
	isSelectedCheck: { default: () => false },
})
const emits = defineEmits(["select"])
const emitSelect = target => emits("select", target)

const loading = ref(false)
const childrens = ref([])
const page = ref(1)
const isExpanded = computed(() => childrens.value && childrens.value.length > 0)
const isSelected = computed(() => props.isSelectedCheck(props.target))

const loadChildrens = async (target, page) => {
	loading.value = true
	childrens.value = await props.getChildrens(target, page)
	loading.value = false
}

const toggleExpand = () => {
	emitSelect(props.target)

	if (childrens.value.length > 0) {
		childrens.value = []
	} else if (props.childrensCount) {
		loadChildrens(props.target)
	}
}

const onPaginate = async () => {
	await loadChildrens(props.target, page.value)
}

onMounted(() => {
	if (props.depth === 0) {
		loadChildrens(props.target)
	}
})

defineExpose({loadChildrens})
</script>
