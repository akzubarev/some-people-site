<template>
  <div class="flex flex-col w-fit md:w-full gap-2">
    <div class="flex flex-row w-full justify-between items-center gap-4">
      <div class="flex flex-row items-center gap-4"
           :class="full ? 'w-[30%]' : 'w-full'">
        <Avatar :username="`${user.first_name} ${user.last_name}`"
                :size="full ? 50 : 25" :showFlag="false" :src="user.avatar"
        />
        <div class="flex justify-start items-start flex-col cursor-pointer">
          <div class="text-white" :class="!full && 'text-sm'"> {{
              `${user.first_name} ${user.last_name}`
            }}
          </div>
          <div class="flex gap-2">
            <div class="text-sm text-gray-400">
              {{ user.username }}
            </div>
          </div>
        </div>
      </div>
      <slot/>
      <div class="flex flex-row items-center justify-between w-[30%] gap-3"
           v-if="full && game">
        <div class="text-sm whitespace-pre-wrap text-center"> Статус: {{
            {
              "pending": "Подана",
              "discussing": "Обсуждается",
              "confirmed": "Принята",
              "declined": "Отклонена",
              "deleted": "Удалена"
            }[application.status]
          }}
        </div>
        <div class="text-sm whitespace-pre-wrap text-center" v-if="full">
          Заполнено {{
            Object.keys(application.answers).length * 100 / questions
          }}%
        </div>
        <button
            v-if="full"
            @click="$router.push(`/game/${game}/application/${user.id}`)"
            class="btn btn flex items-center bg-white hover:bg-gray-500 !p-2">
              <span class="text-center text-sm text-black">
                  Заявка
               </span>
        </button>
      </div>
    </div>
    <hr v-if="full">
  </div>
</template>


<script setup>
import Avatar from "@/components/avatar/Avatar.vue";
import CharacterBlock from "@/views/games/factions/CharacterBlock.vue";

const props = defineProps({
  game: {
    type: String,
    default: null
  },
  user: {
    id: 1,
    first_name: "lorem",
    last_name: "ipsum",
    application: {},
    email: "",
  },
  questions: {
    type: Number,
    default: 10
  },
  full: {
    type: Boolean,
    default: true
  },

})

const application = props.user.applications[props.game]
</script>
