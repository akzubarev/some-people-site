<template>
  <Form class="form" novalidate="novalidate" @submit="saveProfile">
    <div class="card-body flex flex-col w-full gap-3">
      <div class="setting-container">
        <label class="title"> {{ $t("settings.avatar") }} </label>
        <TinyImageUploader
            class="bg-bg-primary !w-[100px] !h-[100px] rounded-full" icon
            :image="avatar || user.avatar" @upload="avatar = $event"
        />
      </div>

      <div class="setting-container">
        <label class="title"> {{ $t("settings.firstNameAndLastName") }} </label>
        <div class="flex flex-row gap-3 basis-2/3">
          <div class="w-full">
            <Field class="form-input" v-model="user.first_name"
                   type="text" name="first_name" :placeholder="$t('user.firstName')"/>
            <span v-if="errors.first_name" class="input-error-message">{{ errors.first_name }}</span>
          </div>
          <div class="w-full">
            <Field class="form-input" v-model="user.last_name"
                   type="text" name="last_name" :placeholder="$t('user.lastName')"/>
            <span v-if="errors.last_name" class="input-error-message">{{ errors.last_name }}</span>
          </div>
        </div>
      </div>

      <div class="setting-container">
        <label class="title"> {{ $t("user.phone") }} </label>
        <Field class="form-input" v-model="user.phone"
               type="text" name="phone" placeholder="+79000000000"/>
        <span v-if="errors.phone" class="input-error-message">{{ errors.phone }}</span>
      </div>

      <div class="setting-container">
        <label class="title"> {{ $t("user.username") }} </label>
        <Field class="form-input" v-model="user.username"
               type="text" name="username" :placeholder="$t('settings.usernamePlaceholder')"/>
        <span v-if="errors.username" class="input-error-message">{{ errors.username }}</span>
      </div>

      <div class="setting-container">
        <label class="title"> Instagram </label>
        <Field class="form-input" v-model="user.instagram"
               type="text" name="instagram" placeholder="@instagram"/>
        <span v-if="errors.instagram" class="input-error-message"> {{ errors.instagram }} </span>
      </div>

      <Telegram/>
      <button
          type="submit" id="kt_account_profile_details_submit"
          class="btn-gray ml-auto w-fit max-sm:w-full">
        <span class="indicator-label"> {{ $t("common.actions.save") }} </span>
      </button>
    </div>
  </Form>
</template>

<style>
.setting-container {
  @apply flex flex-wrap;

  & .title {
    @apply flex text-content-primary items-center basis-full lg:basis-1/3
  }

}
</style>

<script setup>
import formhelper from "@/core/helpers/form"
import {useStore} from "vuex"
import {ref} from "vue"
import {Field, Form} from "vee-validate"
import authService from "@/services/authService"
import {useI18n} from "vue-i18n"
import TinyImageUploader from "@/components/image-uploader/TinyImageUploader.vue"
import Telegram from "@/views/account/settings/Telegram.vue";


const store = useStore()
const user = store.getters["auth/user"]
const form = formhelper()
const {errors} = form
const {t} = useI18n()
const emit = defineEmits(['saved'])

const avatar = ref("")

const saveProfile = values => {
  if (avatar.value) {
    values["avatar"] = avatar.value
  }
  values["country_iso"] = user.country_iso
  values["country"] = user.country
  form.send(async () => {
    await authService.me(values)
    emit('saved')
  })
}

</script>
