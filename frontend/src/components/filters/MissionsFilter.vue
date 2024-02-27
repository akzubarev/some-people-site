<template>
  <div class="flex flex-col mt-3">
    <div
        @click="() => (missionsExpanded = !missionsExpanded)"
        class="flex justify-between items-center pe-2 cursor-pointer"
    >
      <h2 class="form-check-label text-primary cursor-pointer">
        {{ $t("matrix.tree.activeMissions") }}
      </h2>
      <inline-svg
          :class="[s.arrow, { [s.arrow_expanded]: missionsExpanded }]"
          :src="require('@/assets/images/icons/chevrone.svg')"
      />
    </div>
    <div
        class="flex flex-col justify-center transition-all overflow-hidden duration-300 h-0"
        :class="missionsExpanded && '!h-[18rem] pt-4'"
    >
      <ActiveMissionsBlock
          :clear="clear"
          @targets="(t) => {targetMissions=t; $emit('targets', targetMissions)}"
      />
    </div>
  </div>
</template>

<script setup>
import s from "@/components/filters/styles.module.scss";
import ActiveMissionsBlock
  from "@/components/user-modal/ActiveMissionsBlock.vue"
import {ref} from "vue";

const props = defineProps(['clear', 'targetMissions'])
const emit = defineEmits(['targets'])

const targetMissions = ref(props.targetMissions)
const missionsExpanded = ref(true)
const clear = ref(props.clear)
</script>
