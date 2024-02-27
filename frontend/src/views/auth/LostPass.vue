<template>
  <!--begin::Wrapper-->
  <div class="w-lg-500px w-full  rounded shadow-sm p-10 p-lg-15 mx-auto">
    <!--begin::Form-->
    <Form class="form w-full" id="kt_login_signin_form"
          @submit="onSubmitLogin">
      <!--begin::Heading-->
      <div class="text-center mb-10">
        <!--begin::Title-->
        <h1 class="text-dark mb-3">
          {{ $t("auth.lostPassword") }}
        </h1>
      </div>
      <!--end::Input group-->
      <div class="fv-row mb-10">
        <label class="form-label fs-6  text-dark">Email</label>
        <!--begin::Input-->
        <Field
            class="form-control form-control-lg form-control-solid"
            type="email"
            name="email"
            autocomplete="off"
            :placeholder="$t('auth.enterEmail')"
        />
        <!--end::Input-->
        <div class="fv-plugins-message-container">
          <div class="fv-help-block">
            <span>{{ errors.email || "" }}</span>
          </div>
        </div>
      </div>
      <!--begin::Actions-->
      <div class="text-center">
        <!--begin::Submit button-->
        <button
            type="submit"
            id="kt_sign_in_submit"
            class="btn btn-lg btn-primary w-full mb-5"
        >
          <span class="indicator-label">
            {{ $t("common.actions.approve") }}
          </span>
        </button>
        <!--end::Submit button-->
      </div>
      <!--end::Actions-->
    </Form>
    <!--end::Form-->
  </div>
  <!--end::Wrapper-->
</template>

<script lang="ts">
import {defineComponent} from "vue"
import {Form, Field} from "vee-validate"
import authService from "@/services/authService"
import formhelper from "@/core/helpers/form"

export default defineComponent({
  name: "lostpass",
  props: ["uid", "token"],
  components: {
    Form,
    Field
  },
  setup() {
    const form = formhelper()

    const {errors} = form

    const onSubmitLogin = values => {
      form.send(async () => {
        await authService.sendPassReset({
          email: values["email"].trim().toLowerCase()
        })
        setTimeout(() => {
          // Swal.fire({
          //   text: "Инструкция по сбросу пароля была отправлена вам на email.",
          //   icon: "success"
          // })
        }, 200)
      })
    }

    return {
      errors,
      onSubmitLogin
    }
  }
})
</script>
