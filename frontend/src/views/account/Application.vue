<template class="relative">
  <div v-if="!!application.status"
       class="flex flex-col gap-[5%] bg-bg-transparent-white overflow-y-auto no-scrollbar p-6">
    <div class="text-large text-content-secondary"> Заявка {{
        $t(`application.${application.status}`).toLowerCase()
      }}
    </div>
    <div v-if="application.status != 'deleted'" class="flex flex-col gap-[5%]">
      <CharacterBlock v-if="!!application.character" :game_alias="game_alias"
                      :character="application.character" :personal="true"
      />
      <div class="flex flex-row items-center gap-2 text-medium text-content-secondary">
        <inline-svg v-if="!questionnaire_unfilled" class="w-6 h-6"
                    :src="require('@/assets/images/icons/common/check.svg')"/>
        Опросник: {{ !questionnaire_unfilled ? "пройден" : "" }}
        <a v-if="questionnaire_unfilled" class="underline" :href="`/account/${game_alias}/questionnaire`"> заполнить </a>
        <Undone :number="questionnaire_unfilled"/>
      </div>
      <div class="text-medium text-content-secondary font-bold">
        <inline-svg v-if="application.price && application.payed == application.price"
                    class="w-6 h-6" :src="require('@/assets/images/icons/common/check.svg')"/>
        Взнос: {{ application.price ? `${application.payed} / ${application.price}` : 'не объявлен' }}
        <a v-if="application.price && application.payed != application.price" class="underline" href="/"> Оплатить </a>
      </div>
      <div class="flex flex-row items-center gap-2 text-medium text-content-secondary font-bold">
        <inline-svg v-if="!application_unfilled" class="w-6 h-6"
                    :src="require('@/assets/images/icons/common/check.svg')"/>
        Дополнительная информация
        <Undone :number="application_unfilled"/>
      </div>
      <Form v-if="questions.filter(q => q.order < 0)"
            class="form flex flex-col w-full gap-6" novalidate="novalidate" @submit="onSubmit">
        <QuestionField
            v-for="question in questions.filter(q => q.order < 0)" @change="answerUpdate"
            :key="`${question.id} ${default_answers[question.id]}`" :horizontal="false"
            :unfilled="false" :question="question" :errors="errors"
            :default-value="default_answers[question.id]"
        />
      </Form>
      <button @click="onDelete()" class="btn-gradient w-fit text-center text-xl">
        Удалить заявку
      </button>
    </div>
    <button v-else @click="onRestore()" class="btn-gradient w-fit text-center text-xl">
      Восстановить заявку
    </button>
  </div>
  <div v-else class="flex flex-col gap-medium bg-bg-transparent-white overflow-y-auto no-scrollbar p-6">
    <div class="text-large text-content-secondary"> Заявка не подана</div>
    <button ref="submitButton" @click="onSubmit(answers)" class="btn-gradient w-full text-center text-xl">
      Подать заявку
    </button>
  </div>
</template>

<script setup lang="ts">
import {computed, ref} from "vue"
import {useStore} from "vuex"
import {useI18n} from "vue-i18n"
import CharacterBlock from "@/views/games/roles/groups/CharacterBlock.vue";
import gamesService from "@/services/gamesService";
import QuestionField from "@/views/account/questionnaire/QuestionField.vue";
import {Form} from "vee-validate";
import formhelper from "@/core/helpers/form"
import Undone from "@/views/account/drawer/Undone.vue";


const {t} = useI18n()
const store = useStore()

const props = defineProps(["game_alias", "userId"])
const game_alias = props.game_alias
const form = formhelper()
const {errors} = form


const user = computed(() => store.getters["auth/user"])
const user_id = computed(() => props.userId || user.value.id)
const application = computed(() => store.getters["games/application"])
const questions = computed(() => store.getters["games/questions"])

const getApplicationAnswers = (answers) => {
  return Object.fromEntries(Object.entries(answers).filter((q_id, v) => q_id < 0 && !!v))
}
const answers = ref(getApplicationAnswers(application.value.answers?.values || {}))

const default_answers = computed(() => application.value.answers?.values || {})
const questionnaire_unfilled = computed(() =>
    questions.value.filter(q => q.order > 0 && application.value?.answers?.unfilled.includes(q.id)).length
)
const application_unfilled = computed(() =>
    questions.value.filter(q => q.order < 0 && application.value?.answers?.unfilled.includes(q.id)).length
)

const loadData = () => {
  gamesService.application(user_id.value, game_alias).then(({data}) => {
    store.dispatch("games/setApplication", data)
  })
  gamesService.questions(game_alias).then(({data}) => {
    store.dispatch("games/setQuestions", data)
  })
}

const answerUpdate = (field_name, answer) => {
  answers.value[field_name] = answer
}

const onSubmit = (values) => {
  const answersToSend = {...answers.value, game_alias: game_alias}
  form.send(async () => {
    await gamesService.apply(answersToSend)
    loadData()
  })
}

const onLeave = () => {
  const answersToSend = {...answers.value, game_alias: game_alias}
  form.send(async () => {
    await gamesService.apply(answersToSend)
  })
}

const onDelete = () => {
  gamesService.delete_application(game_alias).then(({data}) => {
    loadData()
  })
}

const onRestore = async () => {
  await gamesService.restore_application(game_alias).then(({data}) => {
    loadData()
  })
}

window.addEventListener('beforeunload', onLeave)
</script>
