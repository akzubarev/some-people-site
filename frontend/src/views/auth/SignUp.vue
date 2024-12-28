<template>
  <Form class="form w-full max-w-[500px] flex flex-col items-center overflow-auto no-scrollbar gap-6 p-3"
        novalidate="novalidate" @submit="onSubmitRegister">
    <div class="flex flex-col md:flex-row gap-3">
      <InputField
          :title="$t('user.firstName')" :errors="errors.first_name|| our_errors.first_name"
          name="first_name" placeholder="Имя" :horizontal="false"
      />
      <InputField
          :title="$t('user.lastName')" :errors="errors.first_name|| our_errors.first_name"
          name="last_name" placeholder="Фамилия" :horizontal="false"
      />
    </div>
    <div class="flex flex-col md:flex-row gap-3">
      <InputField
          :title="$t('user.username')" :errors="errors.username|| our_errors.username"
          name="username" :horizontal="false"
      />
      <InputField
          :title="$t('user.email')" :errors="errors.email|| our_errors.email"
          name="email" type="email" placeholder="email" :horizontal="false"
      />
    </div>
    <div class="flex flex-col md:flex-row gap-3">
      <InputField
          :title="$t('common.password')" :errors="errors.password|| our_errors.password"
          name="password" type="password" placeholder="Пароль" :horizontal="false"
      />
      <InputField
          :title="$t('settings.repeatPassword')" :errors="errors.re_password|| our_errors.re_password"
          name="re_password" type="password" placeholder="Повторите пароль" :horizontal="false"
      />
    </div>
    <div class="flex flex-col w-full items-center gap-1">
      <router-link class="text-lg text-active-primary underline" to="/sign-in">
        {{ $t("auth.signIn") }}
      </router-link>
      <button id="kt_sign_up_submit" ref="submitButton" type="submit" class="btn-primary w-full p-3">
        {{ $t("auth.signUp") }}
      </button>
    </div>
  </Form>
</template>

<script setup lang="ts">
import {ref} from "vue"
import {Form} from "vee-validate"
import {useStore} from "vuex"
import {useRouter} from "vue-router"
import authService from "@/services/authService"
import formhelper from "@/core/helpers/form"
import InputField from "@/components/InputField.vue";

const store = useStore()
const router = useRouter()

const submitButton = ref<HTMLElement | null>(null)
const form = formhelper()
const {errors} = form
const our_errors = ref({})

const onSubmitRegister = values => {
  store.dispatch("body/showActionLoader")
  our_errors.value = {}
  form.send(async () => {
    try {
      values.email = (values.email || "").trim()
      const data = (await authService.register(values))["data"]
      if (!Object.keys(errors.value).length) {
        await store.dispatch("auth/setToken", data.auth_token)
        await router.push("/account/settings")
      }
    } catch (error) {
      our_errors.value = error.response.data
    }
    store.dispatch("body/hideActionLoader")
  })
}

</script>
