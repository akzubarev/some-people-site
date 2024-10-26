<template>
  <Popup v-if="user && Object.keys(user).length > 0" @close="$emit('close')">
    <div class="flex flex-col gap-[20px] p-3">
      <div class="flex p-0 pt-4 gap-4">
        <Avatar
            :src="user.avatar"
            :avatar-class="$style.avatar"
            :username="`${user.first_name || '-'} ${user.last_name || '-'}`"
            :country="user.country_iso || 'ru'"
            size="55"
        />
      </div>
    </div>
  </Popup>
</template>

<script setup>
import Avatar from "@/components/Avatar.vue"
import Popup from "@/components/Popup.vue"
import {useI18n} from "vue-i18n"
import {useStore} from "vuex";

const store = useStore()
const {t} = useI18n()
const show = true
const props = defineProps({user: {}})


</script>

<style module lang="scss">
.modal_block {
  @apply bg-[#15171A] rounded-xl flex flex-col gap-[20px] p-4;
}

.link {
  // @apply text-[var(--dark-link-color)];
  @apply text-blue-500;
  a {
    // @apply text-[var(--dark-link-color)];
    @apply text-blue-500;
    &:hover {
      opacity: 0.85;
    }
  }
}

.avatar {
  width: 48px;
  height: 48px;
}
</style>
