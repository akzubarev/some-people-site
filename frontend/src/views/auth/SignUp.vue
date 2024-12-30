<template>
  <Form class="form w-full max-w-[500px] flex flex-col items-center overflow-auto no-scrollbar gap-6 p-3"
        novalidate="novalidate" @submit="onSubmitRegister">
    <div class="input-row">
      <InputField
          :title="$t('user.firstName')" :errors="all_errors.first_name"
          name="first_name" placeholder="Имя" :horizontal="false"
      />
      <InputField
          :title="$t('user.lastName')" :errors="all_errors.last_name"
          name="last_name" placeholder="Фамилия" :horizontal="false"
      />
    </div>
    <div class="input-row">
      <InputField
          :title="$t('user.username')" :errors="all_errors.username"
          name="username" placeholder="Никнейм" :horizontal="false"
      />
      <InputField
          :title="$t('user.email')" :errors="all_errors.email"
          name="email" type="email" placeholder="email" :horizontal="false"
      />
    </div>
    <div class="input-row">
      <InputField
          :title="$t('common.password')" :errors="all_errors.password"
          name="password" type="password" placeholder="Пароль" :horizontal="false"
      />
      <InputField
          :title="$t('settings.repeatPassword')" :errors="all_errors.re_password"
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
import {computed, ref} from "vue"
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
const all_errors = computed(() => {
  return {
    first_name: errors.value.first_name || our_errors.value.first_name,
    last_name: errors.value.last_name || our_errors.value.last_name,
    username: errors.value.username || our_errors.value.username,
    email: errors.value.email || our_errors.value.email,
    password: errors.value.password || our_errors.value.password,
    re_password: errors.value.re_password || our_errors.value.re_password,
  }
})

const onSubmitRegister = values => {
  form.send(async () => {
    our_errors.value = {}
    store.dispatch("body/showActionLoader")
    try {
      values.email = (values.email || "").trim()
      const data = (await authService.register(values))["data"]
      if (!Object.keys(errors.value).length) {
        await store.dispatch("auth/setToken", data.auth_token)
        await router.push("/account/settings")
      }
    } catch (error) {
      Object.entries(error.response.data).forEach(([k, v]) => {
        our_errors.value[k] = Array.isArray(v) ? v[0] : v
      })
    }
    store.dispatch("body/hideActionLoader")
  })
}

</script>

<style scoped>
.input-row {
  @apply flex flex-col md:flex-row w-full gap-3;
}
</style>