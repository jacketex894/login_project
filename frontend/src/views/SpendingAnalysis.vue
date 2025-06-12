<template>
  <div class="wrapper">
    <ExpenseRecorder  @added="handleAdded"/>
    <ItemListMobile v-if="isMobile"  ref="item_list_mobile"/>
    <ItemList v-else ref="item_list"/>
  </div>
</template>

<script>
import ItemList from '@/components/ItemList.vue';
import ItemListMobile from '@/components/ItemListMobile.vue';
import ExpenseRecorder from '@/components/ExpenseRecorder.vue';
export default {
  name: 'SpendingAnalysis',
  components: {
    ItemListMobile,
    ItemList,
    ExpenseRecorder
  },
  data() {
    return {
      isMobile: false
    }
  },
  methods:{
     handleAdded() {
      if (this.isMobile)
        this.$refs.item_list_mobile.showList();
      else
        this.$refs.item_list.showList();
    }
  },
  mounted() {
    this.isMobile = window.innerWidth <= 768;
  }
}
</script>

<style scoped>
.wrapper {
  display: flex;
  justify-content: center;
  flex-direction: row;
}
@media (max-width: 768px) {
  .wrapper {
    flex-direction: column;
    width: 100vw;
  }
  .wrapper > * {
    width: 100%;  
    box-sizing: border-box;
  }
}
</style>