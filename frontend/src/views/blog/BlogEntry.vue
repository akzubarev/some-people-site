<template>
  <div class="card flex gap-6"
       :class="dashboard ?  'flex-col' : 'max-xl:flex-col'">
    <div class="relative w-full "
         :class="!dashboard && 'xl:py-6 xl:ps-6 xl:min-w-[300px] xl:w-fit'"
         v-if="post.preview">
      <!--      aspect-[4/3] -->
      <img
          class="rounded-xl max-xl:rounded-b-none object-cover max-w-none w-full xl:max-h-[17rem]"
          :class="dashboard && 'rounded-b-none'"
          :src="post.preview"/>
      <!--      <div-->
      <!--        v-if="!post.viewed_by_me"-->
      <!--        class="absolute top-[10px] right-[10px] rounded-full w-[20px] h-[20px]-->
      <!--        flex items-center bg-gradient-to-r-->
      <!--        from-[#f1ff00] to-[#dd7007]"-->
      <!--        :class="!dashboard && 'xl:top-[35px]'"-->
      <!--        />-->
      <div
          v-if="!post.viewed_by_me" :class="!dashboard && 'xl:top-[35px]'"
          class="absolute w-fit px-2 py-3 h-[20px] top-[10px] right-[10px]
                rounded-full flex items-center text-[--kt-text-white] gap-1
                bg-gradient-to-r from-[#27a90f] to-[#b9d318]">
          <span style="font-size: .9rem; font-weight: 600; line-height: .9rem">
            NEW
          </span>
      </div>
    </div>
    <div class="card-body flex gap-6 w-full"
         :class="post.preview && (dashboard ? '!pt-0' : 'xl:!ps-0 max-xl:!pt-0')">
      <div
          class="w-full flex flex-col justify-between gap-6 xl:min-w-[300px]">
        <div class="flex flex-col gap-2 h-full">
          <div class="flex gap-2 flex-col">
            <div class="flex gap-2 flex-wrap"
                 v-if="post.tags && post.tags.length">
              <div
                  v-for="(tag, i) in post.tags.slice(0, 5)"
                  :key="i" class="px-2 border border-1 rounded-xl"
                  :style="`border-color: ${tag.color} !important; color: ${tag.color}`">
                <span style="font-size: .9rem; font-weight: 600">
                  {{ tag.name }}
                </span>
              </div>
              <div class="px-2 rounded-xl flex items-center
              border-[1px] border-[grey] text-[grey] gap-1">
                <inline-svg
                    :src="require('@/assets/images/icons/auth/eye.svg')"
                />
                <span
                    style="font-size: .9rem; font-weight: 600; line-height: .9rem">
                    {{ post.viewed }}
                  </span>
              </div>

              <div v-if="post.tags.length > 5"
                   class="px-2 rounded-xl bg-secondary">
                <span style="font-size: .9rem">{{
                    `+${post.tags.length - 5}`
                  }}</span>
              </div>
            </div>
            <div v-if="!post.viewed_by_me && !post.preview"
                 class="rounded-full w-[20px] h-[20px]
              flex items-center bg-gradient-to-r
              from-[--accent-color-start] to-[--accent-color-end]"
            />
            <div class="wrapped-text mb-1 text-2xl text-white">{{
                post.title
              }}
            </div>
          </div>
          <div>
              <span class="wrapped-text wrapped-text-3">{{
                  post.description
                }}</span>
          </div>
        </div>
        <button
            class="btn btn-outline-accent w-[150px] mt-auto"
            @click="() => {$router.push(`/news/${post.id}`)}">
          {{ $t("common.actions.more") }}
        </button>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.wrapped-text {
  &-3 {
    -webkit-line-clamp: 3;
  }

  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  text-overflow: ellipsis;
  overflow: hidden;
}
</style>
<script setup>
const props = defineProps({
  post: {},
  dashboard: {
    type: Boolean,
    default: false
  }
})
</script>
