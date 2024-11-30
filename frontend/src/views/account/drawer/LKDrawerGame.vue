<template>
  <div class="flex flex-col gap-3">
    <div class="flex flex-row gap-2 text-medium items-center uppercase font-bold text-content-secondary cursor-pointer"
         @click="expanded=!expanded">
      <div class="text-sm text-content-secondary" :class="expanded ? 'rotate-90' : ''">▶</div>
      {{ game_title }}
    </div>
    <div v-if="expanded" class="flex flex-col ml-6 gap-1">
      <a class="flex flex-row items-center gap-2 text-medium text-content-secondary"
         :href="`/account/${game_alias}/application`">
        Заявка
        <Undone :number="application_unfilled"/>
      </a>
      <a class="flex flex-row items-center gap-2 text-medium text-content-secondary"
         :href="`/account/${game_alias}/questionnaire`">
        Опросник
        <Undone :number="questionnaire_unfilled"/>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import Undone from "@/views/account/drawer/Undone.vue";
import {computed, ref} from "vue";
import {useStore} from "vuex";

const store = useStore()
const props = defineProps(["game_title", "game_alias"])

const answers = computed(() => store.getters['games/application'].answers)
const questions = computed(() => store.getters['games/questions'])

const questionnaire_unfilled = computed(() =>
    questions.value.filter(q => q.order > 0 && answers.value?.unfilled.includes(q.id)).length
)
const application_unfilled = computed(() =>
    questions.value.filter(q => q.order < 0 && answers.value?.unfilled.includes(q.id)).length
)

const expanded = ref(props.game_alias == 'whales')
</script>