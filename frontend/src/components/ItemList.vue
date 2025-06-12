<template>
  <v-container>
    <v-data-table :headers="headers" :items="items"> 
        <template v-slot:item.date="{ item }">
        <span class="no-wrap">{{ item.date }}</span>
        </template>
    </v-data-table>
  </v-container>
</template>

<script>
import {get_transaction_record} from '@/utils/SpendingAnalysis.js';
export default {
  name: 'ItemList',
  data() {
    return {
      idCounter: 1,
      headers: [
        { title: 'Category', value: 'category' },
        { title: 'Product Name', value: 'product_name' },
        { title: 'Quantity', value: 'quantity' },
        { title: 'Total Cost', value: 'total_cost' ,sortable: true},
        { title: 'Pay By', value: 'pay_by' },
        { title: 'Date', value: 'date',sortable: true},
      ],
      items: []
    }
  },
  methods: {
    async showList() {
      let response =  await get_transaction_record();
      let transactions = response['transactions'];
      for (let i = 0; i < transactions.length; i++) {
        this.items.push(transactions[i]);
      }
    },
  },
  mounted() {
    this.showList();
  }
}
</script>
<style scoped>
.no-wrap {
  white-space: nowrap;
}
</style>
