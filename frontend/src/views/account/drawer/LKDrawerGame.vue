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
        <Undone :number="application_questions-application_answers"/>
      </a>
      <a class="flex flex-row items-center gap-2 text-medium text-content-secondary"
         :href="`/account/${game_alias}/questionnaire`">
        Опросник
        <Undone :number="questionnaire_questions-questionnaire_answers"/>
      </a>
    </div>
  </div>
</template>
<script setup lang="ts">
import Undone from "@/views/account/drawer/Undone.vue";
import {ref} from "vue";
import gamesService from "@/services/gamesService";
import {useStore} from "vuex";

const store = useStore()
const props = defineProps(["game_title", "game_alias"])
const user_id = store.getters['auth/user'].id

const application_questions = ref(0)
const application_answers = ref(0)
const questionnaire_questions = ref(0)
const questionnaire_answers = ref(0)
const expanded = ref(props.game_alias == 'whales')

gamesService.application(user_id, props.game_alias).then(({data}) => {
  const answers =  data.answers
  if (!!answers)
    gamesService.questions(props.game_alias).then(({data}) => {
      const questions = data
      if (!!questions) {
        console.log(Object.entries(answers))
        application_questions.value = questions.filter(q => q.order < 0).length
        questionnaire_questions.value = questions.filter(q => q.order > 0).length
        questionnaire_answers.value = Object.entries(answers).filter((q_id, a) => !!a && questions.find(q => q.id == q_id)?.order > 0).length
        application_answers.value = Object.entries(answers).filter((q_id, a) => !!a && questions.find(q => q.id == q_id)?.order < 0).length
      }
    })
})
</script>