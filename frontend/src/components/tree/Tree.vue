<template>
  <div class="Tree">
    <!--     <span class="fs-2 Tree-Name fw-bold" v-if="depth == 1"
      >Game {{ (matrix.lvl > 3 && -4) + matrix.lvl + 1 }}</span
    > -->
    <div class="w-full">
      <TreeItem
        :matrix="matrix"
        @popup="$emit('popup', $event)"
        @structure="$emit('structure', $event)"
        @deleteBooking="depth >= getDepth() && $emit('deleteBooking', $event)"
        @book="depth >= getDepth() && $emit('book', $event)"
      />
    </div>
    <div :class="`grid mt-5`" :style="`grid-template-columns: repeat(${getDimension()}, minmax(0, 1fr));`">
      <div
        class="w-full"
        v-for="i in getDimension()"
        :key="i"
      >
        <template v-if="depth >= getDepth()">
          <TreeItem
            :matrix="getReferal(i - 1)"
            :canbook="matrix.is_book_available"
            @deleteBooking="$emit('deleteBooking', $event)"
            @book="$emit('book', matrix)"
            @structure="$emit('structure', $event)"
            @popup="$emit('popup', $event)"
          />
          <div class="flex gap-3 justify-center flex-wrap mt-3 px-1">
            <div role="button" :class="[$style.badge_matrix]" 
              v-if="getBonus(i - 1).matrix" @click="$emit('bonusInfo', 'matrix', `${getBonus(i-1).matrix} RSN`, getReferal(i - 1).user)">
                Matrix {{ getBonus(i - 1).matrix }}
            </div>
            <div role="button" :class="[$style.badge_energy]" 
              v-if="getBonus(i - 1).energy" @click="$emit('bonusInfo', 'energy', undefined, getReferal(i - 1).user)">
                Energy
            </div>
            <div role="button" 
              v-if="getBonus(i - 1).nft" :class="[$style.badge_nft]" >
                NFT GEM {{matrix.lvl+1}}
            </div>
            <div role="button" :class="[$style.badge_referal]" 
              v-if="getBonus(i - 1).referal" @click="$emit('bonusInfo', 'referal', `${getBonus(i-1).referal} RSN`, getReferal(i - 1).user)">
                Referal {{ getBonus(i - 1).referal }}
            </div>
            <div role="button" :class="[$style.badge_staking]" 
              v-if="getBonus(i - 1).staking" @click="$emit('bonusInfo', 'staking', `${getBonus(i-1).staking} RSN`, getReferal(i - 1).user)">
                RSD {{ getBonus(i - 1).staking }}
            </div>
            <div
              v-for="(clone, index) in getBonus(i - 1).clones || []"
              :key="index"
              role="button"
            >
              <div
                @click="$emit('bonusInfo', (clone.global ? 'g' : '') + 'clone',
                 `${(clone.global ? 'G' : '')}Clone ${ clone.count } → ${ (clone.lvl > 3 ? clone.lvl - 4 : clone.lvl) + 1}`,
                 getReferal(i - 1).user)"
                :class="[$style.badge_clone]" class="text-nowrap">
                {{ (clone.global && "G") || "" }}Clone {{ clone.count }} →
                {{ (clone.lvl > 3 ? clone.lvl - 4 : clone.lvl) + 1 }}
              </div>
            </div>
          </div>
        </template>
        <template v-else>
          <tree
            :index="i"
            :parent="matrix"
            :matrix="
              getReferal(i - 1) || {
                referals: [],
                lvl: matrix.lvl
              }
            "
            @deleteBooking="$emit('deleteBooking', $event)"
            @book="$emit('book', $event)"
            @structure="$emit('structure', $event)"
            @popup="$emit('popup', $event)"
            @bonusInfo="(b, v, u) => $emit('bonusInfo', b, v, u)"
            :depth="depth + 1"
          />
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { BONUSES } from "@/constants/tree"
import TreeItem from "./TreeItem"
export default {
  name: "tree",
  components: {
    // Avatar,
    TreeItem
  },
  emits: ["popup", "structure", "book", "deleteBooking", "depth", "bonusInfo"],
  props: {
    matrix: {
      type: Object,
      default: () => ({})
    },
    parent: {
      type: Object,
      default: () => ({})
    },
    index: {
      type: Number,
      default: -1
    },
    depth: {
      type: Number,
      default: 1
    }
  },
  setup(props) {
    const getDimension = () => {
      if ([0, 1, 2].includes(props.matrix.lvl)) {
        return 2
      }
      return 3
    }
    const getDepth = () => {
      if ([1, 2].includes(props.matrix.lvl)) {
        return 2
      }
      return 1
    }

    const getBonus = index => {
      let virtualIndex = index
      if (props.index == 2) {
        virtualIndex += 2
      }
      if (props.matrix.lvl == undefined) {
        return {}
      }
      if (props.parent && props.parent.uuid) {
        const spots = (props.matrix.referals || [])
          .filter(m => !m.virtual)
          .map(m => m.uuid)
        if (spots[index]) {
          virtualIndex = [...props.parent.referals_order].indexOf(spots[index])
        } else {
          if (props.index == 1) {
            // console.log(virtualIndex)
            virtualIndex +=
              (props.parent.referals &&
                props.parent.referals[1] &&
                (props.parent.referals[1].referals || []).length) ||
              0
          }
        }
      }
      if (!BONUSES[props.matrix.lvl][getDimension()*getDepth()-1]) {
        BONUSES[props.matrix.lvl][getDimension()*getDepth()-1] = {}
      }
      BONUSES[props.matrix.lvl][getDimension()*getDepth()-1].nft = true
      return BONUSES[props.matrix.lvl][virtualIndex] || {}
    }

    const getReferal = index => {
      const referal = (props.matrix.referals || [])[index]
      if (!referal) {
        const length = (props.matrix.referals || []).length
        let offset = 0
        if (length) {
          offset = (props.matrix.referals[length - 1].virtual && 1) || 0
        }
        return (props.matrix.matrix_request_referals || [])[
          index - (props.matrix.referals || []).length + offset
        ]
      }
      return referal
    }
    // const getChildMatrix = async uuid => {
    //   return (await structureService.matrix.retrieve(uuid)).data
    // }

    const getClones = index => {
      getReferal(index).clones || []
    }

    // const checkChildMatrix = async () => {
    //   if (props.depth >= getDepth()) {
    //     for (const i in [...Array(getDimension()).keys()]) {

    //       childrens.value[getReferal(i).uuid] = await getChildMatrix(getReferal(i).uuid);
    //     }
    //   }
    // }
    // watch(props, 'matrix', v => {
    //   if (v.uuid) {
    //     checkChildMatrix();
    //   }
    // })
    // setTimeout(()=>{
    //   checkChildMatrix()
    // }, 4000)
    return {
      // childrens,
      getReferal,
      getDimension,
      getBonus,
      getClones,
      getDepth
      // getChildMatrix
      // BONUSES
    }
  }
}
</script>
<style lang="scss" module>
 .badge {
   &_matrix {
     color: #009940;
   }
   &_clone {
     color: #CCAA00;
   }
   &_referal {
     color: #0073E5;
   }
   &_energy {
     color: #D93636;
   }
   &_staking {
     color: #D93636;
   }
   &_nft {
     color: #008ba0;
   }
 }
// .modal {
//   background: rgba(0, 0, 0, 0.3);
// }
</style>
<style lang="scss">
@keyframes tree-item-flash {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}
.Tree {
  font-size: 12px;
  position: relative;
  overflow: hidden;
  .Tree {
    overflow: visible;
  }
  // &-Name {
  //   position: absolute;
  //   left: 16px;
  //   top: 16px;
  // }
  &-Avatar {
    z-index: 2;
    max-width: 60px;
    width: 80%;
    @media (min-width: 1140px) {
      max-width: 80px;
    }
    &_Virtual {
      // animation: tree-item-flash 1.5s infinite;
      // box-shadow: 0px 0px 45px 1000px rgba(var(--kt-body-bg-rgb), .5);
      // background-color: var(--kt-danger) !important;
      color: var(--kt-dark) !important;
    }
    // &_Virtual {

    // }
    // height: 10vh !important;
    // width: 10vh !important;
    // @media(min-width: 1140px) {
    //   height: 7vw !important;
    //   width: 7vw !important;
    // }
  }
  &-Username {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  &-Item {
    margin: auto;
    position: relative;
    z-index: 1;
    display: flex;
    justify-content: center;
    // padding: 4px;
    flex-wrap: wrap;
    &_Virtual {
      z-index: 10;
    }
    // &_Me {
    //   &::after {
    //     content: "Я";
    //     position: absolute;
    //     width: 20px;
    //     height: 20px;
    //     background: var(--bs-primary);
    //     color: white;
    //     z-index: 10;
    //     bottom: -2px;
    //     text-align: center;
    //     border-radius: 50%;
    //   }
    // }
  }
}
</style>
