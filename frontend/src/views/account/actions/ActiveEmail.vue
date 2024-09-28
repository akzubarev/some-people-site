<template>
  <div class="card p-6">
    <Form class="form flex flex-col gap-3" novalidate="novalidate" @submit="saveEmail">
      <div class="flex flex-wrap gap-2 justify-between">
          <label class="flex items-center basis-full lg:basis-1/3 required p-0">
            <span v-if="user.email_active" class="fs-5">
            {{ $t("settings.emailConnected") }}
            </span>
            <span class="fs-5" v-else>
              {{ $t("settings.emailDisconnected") }}
            </span>
          </label>

          <div class="basis-full lg:basis-3/5 relative">
            <Field
                type="text"
                name="email"
                class="form-control form-control-lg form-control-solid"
                placeholder="Email"
                readonly
                v-model="user.email"
            />
            <span v-if="errors.email" class="input-error-message">{{ errors.email }}</span>
        </div>
      </div>

      <button
          v-if="!user.email_active"
          type="submit"
          id="kt_account_profile_details_submit"
          ref="submitButton1"
          class="btn btn-primary ml-auto max-sm:w-full"
      >
        <span class="indicator-label" v-if="user.email_active">
          {{ $t("settings.changeEmail") }}
        </span>
        <span class="indicator-label" v-else>
          {{ $t("settings.approveEmail") }}
        </span>
      </button>
    </Form>
  </div>
</template>


<script setup>
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
  const emit = defineEmits(['saved'])

  const saveEmail = values => {
    form.send(async () => {
      await authService.reactivate({
        email: values.email.trim().toLowerCase()
      })
      emit('saved')
    })

  }
</script>
