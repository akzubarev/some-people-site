<template>
  <div class="card p-6">
    <Form class="form flex flex-col gap-3" novalidate="novalidate" @submit="changeEmail">
          <label class="col-form-label required fw-bold p-0">
            {{ $t("settings.changeEmail") }}
          </label>

        <div class="flex max-sm:flex-col gap-3">
          <div class="flex items-center basis-full lg:basis-1/2 relative h-fit">
            <Field
                type="text"
                name="new_email"
                class="form-control form-control-lg form-control-solid"
                :placeholder="$t('settings.newEmail')"
                v-model="new_email"
            />
            <span v-if="errors.new_email" class="input-error-message">{{ errors.new_email }}</span>
          </div>
      </div>

        <button
            type="submit"
            id="kt_account_profile_details_submit"
            ref="submitButton1"
            class="btn btn-primary ml-auto w-fit max-sm:w-full"
        >
            {{ $t("common.actions.change") }}
        </button>
    </Form>
  </div>
</template>


<script setup lang="ts">
  import {ref} from "vue"
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
  const emit = defineEmits(['saved', 'sent', 'error'])

  const new_email = ref('')

  const requestChangeEmail = () => {
    form.send(async () => {
      authService.requestEmailChange({
        email: new_email.value.trim().toLowerCase()
      }).then(function (response) {
        if (response.status < 400) {
          emit('sent')
        } else {
          emit('error')
        }
      }).catch(function (error) {
        emit('error')
      })
    })
  }
  const changeEmail = values => {
    form.send(async () => {
      await authService.changeEmail({
        email: values.new_email.trim().toLowerCase(),
        old_otp: values.old_otp.trim().toLowerCase(),
        new_otp: values.new_otp.trim().toLowerCase(),
      }).then(function (response) {
        if (response.status < 400) {
          user.email = new_email.value
          emit('saved')
        } else {
          emit('error')
        }
      }).catch(function (error) {
        emit('error')
      })
    })
  }
</script>
