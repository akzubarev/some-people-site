<template>
  <ActionModal
      v-if="showLocked" type="lock"
      @close="() => {showLocked = false}"
      @submit="() => {showLocked = false}"
      :title="lockedText" :buttonText="$t('common.actions.ok')">
  </ActionModal>
  <div class="MatrixHeader-Top flex flex-wrap justify-between">
    <div class="card-header !ps-0 !pb-0">
      <div class="card-title text-2xl">{{ title }}</div>
    </div>
    <!--    <div class="MatrixHeader-Menu w-full my-6">-->
    <!--      <ul-->
    <!--          class="flex flex-row gap-1 bg-gray-800 rounded-xl justify-between"-->
    <!--          style="overflow-x: auto; overflow-y: hidden;"-->
    <!--      >-->
    <!--        <li class="nav-item" v-for="page in config" :key="page.title">-->
    <!--          <button-->
    <!--              @click="$router.push(page.link)"-->
    <!--              class="btn flex w-full justify-center text-xl text-active-primary"-->
    <!--              :class="$route.path.includes(page.link) ? 'btn-accent':'btn-outline !border-0'">-->
    <!--            {{ page.title }}-->
    <!--          </button>-->
    <!--        </li>-->
    <!--      </ul>-->
    <!--    </div>-->
    <div class="MatrixHeader-Menu w-full">
      <ul
          class="nav nav-stretch nav-line-tabs nav-line-tabs-2x
          border-transparent !flex-nowrap hide-scrollbar"
          style="overflow-x: auto; overflow-y: hidden;"
      >
        <li v-for="page in config" :key="page" class="nav-item"
            @click="page.locked && lockedSection(page.lockedText)">
          <router-link
              :to=page.link active-class="active"
              class="nav-link text-active-primary me-6"
              :class="[
              'nav-link text-active-primary me-6',
               $route.path.includes(page.link) && 'active',
               page.locked && 'disabled'
            ]">
            <inline-svg v-if="page.locked"
                        :src="require('@/assets/images/icons/matrix/Lock.svg')"/>
            {{ page.title }}
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>


<script setup>
import {useI18n} from "vue-i18n"
import ActionModal from "@/components/action-modal/ActionModal.vue";
import {ref} from "vue";


const props = defineProps(["alias", "config", "title"])
const {t} = useI18n()
const lockedText = ref("Раздел в разработке")
const showLocked = ref(false)

const lockedSection = (text) => {
  lockedText.value = text
  showLocked.value = true
}
</script>


<style lang="scss">
.nav-item {
  margin-bottom: 0px !important;
}

.hide-scrollbar {
  &::-webkit-scrollbar {
    display: none;
  }

  scrollbar-width: none;
  -ms-overflow-style: none;
}
</style>

<style lang="scss">
.MatrixHeader {
  &-Top {
    @apply px-6;
    border-bottom: 1px solid var(--kt-primary-light);
    align-items: center;
    // @media(min-width: 992px) {
    //   padding-top: 18px
    // }
  }

  &-Menu {
    margin-bottom: -3px;
  }

  &-Title {
    color: #6c6f73;
    height: 25px;
    text-align: left;
  }

  &-List {
    display: flex;
    overflow-x: auto;
    justify-content: space-between;

    swiper-slide {
      @media (max-width: 768px) {
        width: 56px;
      }
      text-align: center;
    }
  }

  &-Num {
    font-weight: medium;
    font-size: 24px;
    line-height: 30px;
  }

  &-Item {
    border-radius: 8px;
    cursor: pointer;
    height: 76px;
    width: 56px;
    padding-top: 4px;
    cursor: pointer;
    // &_Active {
    //   background: #141F33;
    // }
  }
}
</style>