<template>
  <Form class="form flex flex-col gap-3" novalidate="novalidate" @submit="savePassword">
    <label class="flex items-center text-content-primary"> {{ $t("settings.changePassword") }} </label>
    <div class="flex max-sm:flex-col gap-3">
      <div class="relative basis-full lg:basis-1/3">
        <Field type="text" name="current_password" class="form-input"
               :placeholder="$t('settings.currentPassword')"/>
        <span v-if="errors.current_password" class="input-error-message">{{ errors.current_password }}</span>
      </div>
      <div class="relative basis-full lg:basis-1/3">
        <Field type="text" name="new_password" class="form-input"
               :placeholder="$t('settings.enterNewPassword')"/>
        <span v-if="errors.new_password" class="input-error-message">{{ errors.new_password }}</span>
      </div>
      <div class="relative basis-full lg:basis-1/3">
        <Field type="text" name="re_password" class="form-input"
               :placeholder="$t('settings.repeatPassword')"/>
        <span v-if="errors.re_password" class="input-error-message">{{ errors.re_password }}</span>
      </div>
    </div>
    <button type="submit" id="kt_account_profile_details_submit" ref="submitButton1"
            class="btn-gray ml-auto w-fit max-sm:w-full">
      {{ $t("common.actions.change") }}
    </button>
  </Form>
</template>


<script setup>
import {Field, Form} from "vee-validate"
import {useI18n} from "vue-i18n"
import {useStore} from "vuex"
import authService from "@/services/authService"
import formhelper from "@/core/helpers/form"


const store = useStore()
const user = store.getters["auth/user"]
const form = formhelper()
const {errors} = form
const {t} = useI18n()
const emit = defineEmits(['saved', 'error'])

const savePassword = values => {
  if (values["new_password"] != values["re_password"]) {
    errors.value["re_password"] = t("settings.passwordDoesnotMatch")
    emit('error')
    return
  }
  form.send(async () => {
    await authService.changePassword({
      new_password: values["new_password"],
      current_password: values["current_password"]
    })
    emit('saved')
  })
}
</script>
