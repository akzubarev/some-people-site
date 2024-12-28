<template class="relative">
  <div v-if="!!application.status"
       class="flex flex-col gap-6 md:bg-bg-transparent-white overflow-y-auto no-scrollbar">
    <div class="text-large px-6 md:px-0 text-content-secondary"> Заявка {{
        $t(`application.${application.status}`).toLowerCase()
      }}
    </div>
    <div v-if="application.status != 'deleted'" class="flex flex-col gap-[5%]">
      <CharacterBlock v-if="!!application.character" :game_alias="game_alias"
                      :character="application.character" :personal="true"
      />
      <div class="flex flex-col gap-[5%] px-6 md:px-0">
        <div class="flex flex-row items-center gap-2 text-medium text-content-secondary"
             :class="questionnaire_unfilled ? 'font-bold' : ''">
          Опросник: {{ !questionnaire_unfilled ? "пройден" : "" }}
          <a v-if="questionnaire_unfilled" class="underline" :href="`/account/${game_alias}/questionnaire`">
            заполнить </a>
          <inline-svg v-else class="w-6 h-6" :src="require('@/assets/images/icons/common/check.svg')"/>
          <Undone :number="questionnaire_unfilled"/>
        </div>
        <div class="text-medium text-content-secondary"
             :class="(application.price && application.payed<application.price) ? 'font-bold' : ''">
          Взнос: {{ application.price ? `${application.payed} / ${application.price}` : 'не объявлен' }}
          <inline-svg v-if="application.price && application.payed == application.price"
                      class="w-6 h-6" :src="require('@/assets/images/icons/common/check.svg')"/>
          <a v-if="application.price && application.payed != application.price" class="underline" href="/"> Оплатить </a>
        </div>
        <div class="flex flex-row items-center gap-2 text-medium text-content-secondary font-bold"
             :class="application_unfilled ? 'font-bold' : ''">
          Дополнительная информация
          <inline-svg v-if="!application_unfilled" class="w-6 h-6"
                      :src="require('@/assets/images/icons/common/check.svg')"/>
          <Undone :number="application_unfilled"/>
        </div>
        <Form
            v-if="questions.filter(q => q.order < 0) && (Object.keys(default_answers).length + application_unfilled)"
            class="form flex flex-col w-full gap-6" novalidate="novalidate" @submit="onSubmit">
          <QuestionField
              v-for="question in questions.filter(q => q.order < 0)"
              :key="question.id" :horizontal="false" @change="answerUpdate"
              :unfilled="false" :question="question" :errors="errors"
              :default-value="default_answers[question.id]"
          />
        </Form>
        <button @click="onDelete()" class="btn-primary w-fit text-center text-xl">
          Удалить заявку
        </button>
      </div>
    </div>
    <button v-else @click="onRestore()" class="btn-primary w-fit text-center text-xl p-3 mx-6 md:mx-0">
      Восстановить заявку
    </button>
  </div>
  <div v-else class="flex flex-col gap-medium md:bg-bg-transparent-white overflow-y-auto no-scrollbar p-6">
    <div class="text-large text-content-secondary"> Заявка не подана</div>
    <button ref="submitButton" @click="onSubmit(answers)" class="btn-primary w-full p-3 text-center text-xl">
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
const application = computed(() => store.getters["games/application"])
const questions = computed(() => store.getters["games/questions"])

const getApplicationAnswers = (answers) => {
  return Object.fromEntries(
      Object.entries(answers).filter(
          (q_id, v) => questions.value.find((q) => q.id == q_id)?.order < 0 && !!v
      )
  )
}
const answers = ref(getApplicationAnswers(store.getters['games/answers'].values))
const default_answers = computed(() => store.getters['games/answers'].values)
const questionnaire_unfilled = computed(() => store.getters['games/questionnaire_unfilled'])
const application_unfilled = computed(() => store.getters['games/application_unfilled'])

const answerUpdate = (field_name: string, answer, true_update: boolean) => {
  answers.value[field_name] = answer
  if (true_update)
    onInput()
}

const onSubmit = (values = {}) => {
  const answersToSend = {...answers.value, game_alias: game_alias}
  form.send(async () => {
    gamesService.apply(answersToSend).then(({data}) => {
      store.dispatch("games/setApplication", data)
    })
  })
}

const noApplication = () => {
  return ['deleted', '', null].includes(application.value.status)
}

const onDelete = () => {
  gamesService.delete_application(game_alias).then(({data}) => {
    store.dispatch("games/setApplication", data)
  })
}

const onRestore = async () => {
  await gamesService.restore_application(game_alias).then(({data}) => {
    store.dispatch("games/setApplication", data)
  })
}

let timer;
const onInput = (force: boolean = false) => {
  if (timer)
    clearTimeout(timer);
  if (force)
    onSubmit()
  else
    timer = setTimeout(onSubmit, 1000)
}
const onLeave = () => {
  if (!noApplication)
    onInput(true)
  window.removeEventListener('beforeunload', onLeave)
}

window.addEventListener('beforeunload', onLeave)
</script>
