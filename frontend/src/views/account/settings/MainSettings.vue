<template>
  <Form class="form" novalidate="novalidate" @submit="saveProfile">
    <div class="card-body flex flex-col w-full gap-3">
      <div class="setting-container">
        <label class="title"> {{ $t("settings.avatar") }} </label>
        <div class="inputs">
          <TinyImageUploader
              class="bg-light-primary w-[100px] !h-[100px] rounded-full"
              icon :image="avatar || user.avatar" @upload="avatar = $event"
          />
        </div>
      </div>

      <div class="setting-container">
        <label class="title"> {{ $t("settings.firstNameAndLastName") }} </label>
        <div class="inputs gap-3">
          <div class="relative w-full">
            <Field
                type="text" name="first_name" v-model="user.first_name"
                class="form-control form-control-lg form-control-solid"
                :placeholder="$t('user.firstName')"
            />
            <span v-if="errors.first_name" class="input-error-message">{{ errors.first_name }}</span>
          </div>

          <div class="relative w-full">
            <Field
                type="text" name="last_name" v-model="user.last_name"
                class="form-control form-control-lg form-control-solid"
                :placeholder="$t('user.lastName')"
            />
            <span v-if="errors.last_name" class="input-error-message">{{ errors.last_name }}</span>
          </div>

        </div>
      </div>

      <div class="setting-container">
        <label class="title"> {{ $t("user.phone") }} </label>
        <div class="inputs">
          <Field
              type="text" name="phone" v-model="user.phone"
              class="form-control form-control-lg form-control-solid"
              placeholder="+79000000000"
          />
          <span v-if="errors.phone" class="input-error-message">{{ errors.phone }}</span>
        </div>
      </div>

      <div class="setting-container">
        <label class="title"> {{ $t("user.username") }} </label>
        <div class="inputs">
          <Field
              type="text" name="username" v-model="user.username"
              class="form-control form-control-lg form-control-solid"
              :placeholder="$t('settings.usernamePlaceholder')"
          />
          <span v-if="errors.username" class="input-error-message">{{ errors.username }}</span>
        </div>
      </div>

      <div class="setting-container">
        <label class="title"> Instagram </label>
        <div class="inputs">
          <Field
              type="text" name="instagram" v-model="user.instagram"
              class="form-control form-control-lg form-control-solid"
              placeholder="@instagram"
          />
          <span v-if="errors.instagram" class="input-error-message"> {{ errors.instagram }} </span>
        </div>
      </div>

      <Telegram/>
      <button
          type="submit" id="kt_account_profile_details_submit"
          class="btn btn-primary ml-auto w-fit max-sm:w-full">
        <span class="indicator-label"> {{ $t("common.actions.save") }} </span>
      </button>
    </div>
  </Form>
</template>

<style scoped lang="scss">
.setting-container {
  @apply flex flex-wrap;
  & .title {
    @apply flex items-center basis-full lg:basis-1/3
  }

  & .inputs {
    @apply flex flex-row items-center basis-full lg:basis-2/3 mt-2 lg:mt-0
  }
}
</style>

<script setup>
import formhelper from "@/core/helpers/form"
import {useStore} from "vuex"
import {ref} from "vue"
import {Field, Form} from "vee-validate"
// import LangSwitcher from "@/components/langswitcher"
// import CountrySwitcher from "@/components/countryswitcher"
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
  if (values.staking_active == "on") {
    values["staking_active"] = false
  } else {
    values["staking_active"] = true
  }
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
