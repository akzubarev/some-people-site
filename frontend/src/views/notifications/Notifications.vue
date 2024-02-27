<template>
  <div class="card">
    <div class="card-header border-0 ">
      <div class="card-title">
        {{ $t("notifications.title") }}
      </div>
    </div>
  </div>
  <template v-for="(notify, index) in [noViewed, viewed]" :key="index">
    <div class="flex flex-col gap-6 mt-6" v-if="notify && notify.length">
      <div class="mx-4">
        <span v-if="index && notify.length" class="text-xl">
          {{ $t("common.history") }}
        </span>
        <span v-if="!index && notify.length">
          {{ $t("common.new") }}
        </span>
      </div>
      <div class="card" v-for="(item, index) in notify" :key="index">
        <div class="card-body">
          <div class="flex flex-col gap-3" v-if="item && item.type">
            <div class="flex justify-between gap-6">
              <div class="text-bold text-white" v-html="item.type.title"/>
              <div class="text-gray-600 whitespace-nowrap">
                {{ timeAgo.format(new Date(item.created_at)) }}
              </div>
            </div>
            <div
                v-if="item && item.type" class="text-gray-500"
                style="word-break: break-word;"
                v-html="item.type.description"
            />
          </div>
        </div>
      </div>
    </div>
  </template>
</template>

<script>
import {defineComponent, ref} from "vue"
import TimeAgo from "javascript-time-ago"
import en from "javascript-time-ago/locale/en"
import notificationService from "@/services/notificationService"

TimeAgo.addLocale(en)
const timeAgo = new TimeAgo("en-US")

export default defineComponent({
  name: "notifications",
  components: {},
  setup() {
    const viewed = ref([])
    const noViewed = ref([])

    ;(async () => {
      const notifications = (await notificationService.list())["data"].results
      viewed.value = notifications.filter(e => e.type && e.viewed)
      noViewed.value = notifications.filter(e => e.type && !e.viewed)
      await notificationService.viewed()
    })()
    return {
      viewed,
      noViewed,
      timeAgo
    }
  }
})
</script>
