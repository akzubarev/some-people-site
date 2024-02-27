<template>
  <div class="w-lg-500px rounded shadow-sm p-10 p-lg-15 mx-auto">
    <!-- Выход из системы -->
  </div>
</template>
<script lang="ts">
import { defineComponent } from "vue"
import { useStore } from "vuex"
import { useRouter } from "vue-router"

export default defineComponent({
  name: "sign-out",
  setup() {
    const store = useStore()
    const router = useRouter()

    store.dispatch("auth/logout")
    router.push({ name: "sign-in" })
  }
})
</script>
