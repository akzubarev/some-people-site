<template>
  <div class="card">
    <div class="card-header border-0">
      <div class="card-title">
        {{ $t("menu.news") }}
      </div>
    </div>
  </div>

  <div
      v-if="posts.length < 1"
      class="w-full flex justify-center items-center mt-6"
      style="height: 50vh"
  >
    {{ "No News" }}
  </div>
  <div class="flex flex-col gap-6 mt-6">
    <BlogEntry
        v-for="(post, i) in posts" :key="`post-${i}`"
        :post="post"
    />
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

<script>
import {defineComponent, ref} from "vue"
import blogService from "@/services/blogService"
import BlogEntry from "@/views/blog/BlogEntry.vue";
import {useStore} from "vuex";

export default defineComponent({
  name: "blog-list",
  components: {BlogEntry},
  setup() {
    const posts = ref([])
    const store = useStore()
    const lang = store.getters['auth/user'].locale || "en"
    const loadPosts = async page => {
      const postsData = (await blogService.list({page})).data
      posts.value = postsData.map(p => ({
        ...p,
        /* preview: p.preview.replace('frontend.admin:8000', 'localhost:8083'), */
        tags: [
          ...p.tags,
          {
            name: new Date(p.created_at).toLocaleDateString(lang, {
              day: "numeric", month: "long"
            }), color: "#777"
          },
        ]
      }))
    }
    loadPosts()
    return {
      posts,
    }
  }
})
</script>
