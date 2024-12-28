<template>
  <Form class="form" novalidate="novalidate" @submit="saveProfile">
    <div class="flex flex-col w-full gap-3">
      <div class="hidden md:flex flex-row w-full items-center gap-6">
        <label class="text-xl"> {{ $t("settings.avatar") }} </label>
        <TinyImageUploader
            icon class="bg-bg-primary !w-[100px] !h-[100px] rounded-full"
            :image="user.avatar" @upload="uploadAvatar = $event; user.avatar = uploadAvatar; inputEvent()"
        />
      </div>
      <div class="flex md:hidden text-lg text-content-disabled w-full">
        Поменять аватар пока что можно только в десктопной версии
      </div>
      <div class="flex flex-col items-center gap-3">
        <div class="settings-row">
          <InputField
              :title="$t('user.firstName')" :errors="errors.first_name"
              name="first_name" :horizontal="false" :v_model="user.first_name"
              placeholder="Имя" @input="inputEvent"
          />
          <InputField
              :title="$t('user.lastName')" :errors="errors.last_name"
              name="last_name" :horizontal="false" :v_model="user.last_name"
              placeholder="Фамилия" @input="inputEvent"
          />
        </div>
        <div class="settings-row">
          <InputField
              :title="$t('user.username')" :errors="errors.username"
              name="username" :horizontal="false" :v_model="user.username"
              :placeholder="$t('settings.usernamePlaceholder')"
          />
          <InputField
              :title="$t('user.email')" :errors="errors.email"
              name="email" :horizontal="false" :v_model="user.email"
              :placeholder="$t('user.email')" @input="inputEvent"
          />
        </div>
        <div class="settings-row">
          <InputField
              :title="$t('user.phone')" :errors="errors.phone"
              name="phone" :horizontal="false" :v_model="user.phone"
              placeholder="+79000000000" @input="inputEvent"
          />
          <InputField
              title="Vk" :errors="errors.vk"
              name="vk" :horizontal="false" :v_model="user.vk"
              placeholder="@vk" @input="inputEvent"
          >
            <div class="text-content-shadowed">Часть после vk.com/</div>
          </InputField>
        </div>
        <div class="flex flex-col w-full gap-1">
          <div class="flex text-xl"> Показывать в сетке ролей</div>
          <div class="flex flex-row items-center gap-3" @click="user.tg_public=!user.tg_public">
            <input type="checkbox" class="form-check-input m-0 w-[20px]" name="checkbox_tg"
                   :checked="user.tg_public" id="checkbox_tg">
            <div class="flex items-center text-xl">ТГ</div>
          </div>
          <div class="flex flex-row items-center gap-3" @click="user.vk_public=!user.vk_public">
            <input type="checkbox" class="form-check-input m-0 w-[20px]" name="checkbox_vk"
                   :checked="user.vk_public" id="checkbox_vk">
            <div class="flex items-center text-xl">ВК</div>
          </div>
        </div>
        <!--        <button type="submit" id="kt_account_profile_details_submit" class="btn-primary ml-auto w-fit max-sm:w-full">-->
        <!--          <span class="indicator-label"> {{ $t("common.actions.save") }} </span>-->
        <!--        </button>-->
      </div>
    </div>
  </Form>
</template>

<script setup lang="ts">
import formhelper from "@/core/helpers/form"
import {useStore} from "vuex"
import {computed, ref} from "vue"
import {Form} from "vee-validate"
import authService from "@/services/authService"
import {useI18n} from "vue-i18n"
import TinyImageUploader from "@/components/image-uploader/TinyImageUploader.vue"
import InputField from "@/components/InputField.vue";


const store = useStore()
const form = formhelper()
const {errors} = form
const {t} = useI18n()
const emit = defineEmits(['saved'])
const user = computed(() => store.getters["auth/user"])
const uploadAvatar = ref(null)

const saveProfile = (values) => {
  form.send(async () => {
    if (!!uploadAvatar.value)
      values.avatar = uploadAvatar.value
    const response = await authService.update_me(values)
    await store.dispatch('auth/setUser', response.data)
    emit('saved')
  })
}

let timer;

const inputEvent = (...args) => {
  onInput()
}

const onInput = (force: boolean = false) => {
  if (timer)
    clearTimeout(timer);
  if (force)
    saveProfile(user.value || {})
  else
    timer = setTimeout(saveProfile, 1000)
}
const onLeave = () => {
  onInput(true)
  window.removeEventListener('beforeunload', onLeave)
}


window.addEventListener('beforeunload', onLeave)
</script>

<style scoped>
.settings-row {
  @apply flex flex-col md:flex-row w-full items-center gap-3;
}
</style>