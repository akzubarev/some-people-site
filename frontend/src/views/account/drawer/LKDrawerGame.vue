<template>
  <div class="flex flex-col gap-3">
    <ActionModal
        v-if="showLocked" type="lock"
        @close="() => {showLocked = false}"
        @submit="() => {showLocked = false}"
        title="Заявка не подана" :buttonText="$t('common.actions.ok')">
    </ActionModal>
    <div class="flex flex-row gap-2 text-medium items-center uppercase font-bold text-content-secondary cursor-pointer"
         @click="expanded=!expanded">
      <div class="text-sm text-content-secondary" :class="expanded ? 'rotate-90' : ''">▶</div>
      {{ game_title }}
    </div>
    <div v-if="expanded" class="flex flex-col ml-6 gap-1">
      <div class="flex flex-row items-center gap-2 text-medium text-content-secondary cursor-pointer"
           @click="()=> openApplication(game_alias)">
        Заявка
        <Undone :number="application_unfilled"/>
      </div>
      <div @click="openQuestionnaire(game_alias)"
           class="flex flex-row items-center gap-2 text-medium cursor-pointer text-content-secondary">
        <inline-svg
            v-if="noApplication()" class="h-6 w-6 text-content-secondary-shadowed"
            :src="require('@/assets/images/icons/common/lock.svg')"/>
        Опросник
        <Undone :number="questionnaire_unfilled"/>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Undone from "@/views/account/drawer/Undone.vue";
import {computed, ref} from "vue";
import {useStore} from "vuex";
import ActionModal from "@/components/ActionModal.vue";
import {useRouter} from "vue-router";

const store = useStore()
const router = useRouter()
const emit = defineEmits(["closeDrawer"])
const props = defineProps(["game_title", "game_alias"])

const questions = computed(() => store.getters['games/questions'])
const application = computed(() => store.getters['games/application'])
const questionnaire_unfilled = computed(() => store.getters['games/questionnaire_unfilled'])
const application_unfilled = computed(() => store.getters['games/application_unfilled'])
const expanded = ref(props.game_alias == 'whales')

const showLocked = ref(false)

const noApplication = () => {
  return ['deleted', null].includes(application.value.status)
}
const openQuestionnaire = (game_alias) => {
  if (noApplication())
    showLocked.value = true
  else {
    emit('closeDrawer')
    router.push(`/account/${game_alias}/questionnaire`)
  }
}
const openApplication = (game_alias) => {
  emit('closeDrawer')
  router.push(`/account/${game_alias}/application`)
}
</script>