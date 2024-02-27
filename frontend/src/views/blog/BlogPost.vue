<template>
  <div class="card mb-5">
    <div class="card-body flex flex-col border-0 gap-6">
      <div class="flex m-0 gap-2 justify-between">
        <button
            @click="$router.back()"
            class="btn nav-link text-active-primary p-0 flex gap-2 items-center"
            style="background-color: transparent"
        >
          <svg
              height="14"
              class="d-block pe-3"
              style="transform: rotate(180deg)"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 26 26"
              fill="#3150f6"
          >
            <path
                d="M 7.023438 3 L 4 5.015625 L 9.519531 13 L 4 20.984375 L 7.023438 23 L 14.019531 13 Z M 15.039063 3 L 11.980469 5.015625 L 17.5 13 L 11.980469 20.984375 L 15.039063 23 L 22 13 Z"
                fill="#3150f6"
            ></path>
          </svg>
          {{ $t('common.actions.back') }}
        </button>
      </div>
      <div class="w-full flex justify-center">
        <img
            class="rounded-xl h-100"
            :src="post.preview"
            style="object-fit: contain; width: inherit"
        />
      </div>
      <div class="flex gap-4 flex-wrap">
        <div
            v-for="(tag, i) in post.tags.slice(0, 5)"
            :key="i"
            class="px-2 border border-1 rounded-xl"
            :style="
            `border-color: ${tag.color} !important; color: ${tag.color}`
          "
        >
          <span style="font-size: .9rem; font-weight: 600">{{
              tag.name
            }}</span>
        </div>
        <div v-if="post.tags.length > 5" class="px-2 rounded-xl">
          <span style="font-size: .9rem">{{
              `+${post.tags.length - 5}`
            }}</span>
        </div>
      </div>
      <div class="flex flex-row gap-2 h-100 items-center">
        <div class="m-0 news-title">{{ post.title }}</div>
      </div>
    </div>
    <div class="card-body pt-0">
      <div ref="postDiv"/>
      <button
          @click="copyShareLink"
          class="btn btn-secondary w-full md:w-auto text-active-primary mt-8 flex gap-2 items-center justify-center"
      >
        <inline-svg class="me-1 w-[1rem]"
                    :src="require('@/assets/images/icons/share.svg')"/>
        {{ $t('common.actions.share') }}
      </button>
    </div>
  </div>
</template>

<style>
.news-title {
  font-size: 1.5rem;
  color: var(--kt-white)
}

@media (min-width: 375px) {
  .news-title {
    font-size: 1.8rem;
  }
}

@media (min-width: 675px) {
  .news-title {
    font-size: 2rem;
  }
}
</style>

<script>
import {defineComponent, ref, onMounted} from "vue"
import blogService from "@/services/blogService"
import {useRoute} from 'vue-router'
import {useI18n} from 'vue-i18n'
import {toClipboard} from "@soerenmartius/vue3-clipboard"
import {useStore} from "vuex";

export default defineComponent({
  name: "blog-list",
  props: ["id"],
  setup(props) {
    const post = ref({tags: []})
    const postDiv = ref({})
    const route = useRoute();
    const t = useI18n().t;
    const store = useStore()

    const lang = store.getters['auth/user'].locale || "en"
    const loadPost = async () => {
      const postData = (await blogService.post(props.id)).data

      post.value = postData
      console.log(postData.created_at, new Date(postData.created_at))
      post.value.tags.unshift({
        name: new Date(postData.created_at).toLocaleDateString(lang, {
          day: "numeric",
          month: "long",
          hour: "numeric",
          minute: "numeric"
        }),
        color: "#777"
      })
      postDiv.value.innerHTML = postData.post
    }

    onMounted(() => loadPost())

    const copyShareLink = async () => {
      if (typeof navigator.share !== 'function') {
        toClipboard(window.location.href)
        // Swal.fire({
        //   icon: "success",
        //   text: t('common.linkCopied')
        // })
      } else {
        const blob = await (await fetch(post.value.preview)).blob()
        const data = {
          text: `${post.value.title}\n${window.location.href}`,
          // url: post.value.preview,
          files: [new File([blob], 'preview.png', {type: blob.type})],
        }
        const availableData = {}
        Object.entries(data).forEach(([key, value]) => {
          if (navigator.canShare({[key]: value}))
            availableData[key] = value
        });
        console.log(availableData)
        await navigator.share(availableData)
      }
    }

    return {
      post,
      postDiv,
      copyShareLink
    }
  }
})
</script>
