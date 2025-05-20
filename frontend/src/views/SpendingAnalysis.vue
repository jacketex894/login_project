<template>
  <v-card class = "transaction-container">
    <v-card-title class="headline">消費紀錄</v-card-title>
    <v-divider></v-divider>

    <v-form v-model="valid" ref="form" lazy-validation class="pa-4">
      <v-text-field
        v-model="form.category"
        label="分類"
        :rules="[rules.required]"
        outlined
        dense
      />

      <v-text-field
        v-model="form.product_name"
        label="產品名稱"
        :rules="[rules.required]"
        outlined
        dense
      />

      <v-text-field
        v-model.number="form.quantity"
        label="數量"
        type="number"
        :rules="[rules.required, rules.min(1)]"
        outlined
        dense
      />

      <v-text-field
        v-model.number="form.total_cost"
        label="總花費"
        type="number"
        :rules="[rules.required, rules.min(0)]"
        outlined
        dense
      />

      <v-select
        v-model="form.pay_by"
        :items="payMethods"
        label="付款方式"
        :rules="[rules.required]"
        outlined
        dense
      />

      <v-menu
        v-model="menu"
        :close-on-content-click="false"
        transition="scale-transition"
        offset-y
        min-width="auto"
      >
        <template #activator="{ props }">
          <v-text-field
            v-model="form.date"
            label="日期"
            prepend-icon="mdi-calendar"
            readonly
            v-bind="props"
            outlined
            dense
          />
        </template>
        <v-date-picker v-model="form.date" @input="menu = false" />
      </v-menu>

      <v-btn
        class="mt-4"
        color="primary"
        :disabled="!valid"
        block
        @click="handleSubmit"
      >
        提交
      </v-btn>
    </v-form>

    <v-alert
            v-if="showAlert"
            :type="alertType"
            colored-border
            class = "alert"
            closable
            @click:close="showAlert = false"
            >
            {{ alertMessage }}
    </v-alert>
  </v-card>
</template>

<script>
import {create_transaction_record} from '@/utils/SpendingAnalysis.js'
export default {
  name: 'SpendingAnalysis',
  data() {
    return {
        valid: false,
        menu: false,
        form:{
            category: '',
            product_name: '',
            quantity: 1,
            total_cost: 0,
            pay_by: '',
            date: this.getTodayDate()
        },
        payMethods: ['Cash', 'Card', 'Other'],
        rules: {
            required: v => !!v || '此欄位為必填',
            min: min => v => v >= min || `數值需 ≥ ${min}`
        },
        showAlert:false,
        alertMessage:null,
        alertType:null,
    }
  },
  methods: {
    getTodayDate() {
      const today = new Date();

      const yyyy = today.getFullYear();
      const mm = String(today.getMonth() + 1).padStart(2, '0');
      const dd = String(today.getDate()).padStart(2, '0');

      const hh = String(today.getHours()).padStart(2, '0');
      const min = String(today.getMinutes()).padStart(2, '0');
      const ss = String(today.getSeconds()).padStart(2, '0');

      return `${yyyy}-${mm}-${dd} ${hh}:${min}:${ss}`;
    },
    async handleSubmit() {
        if (this.valid) {
          this.submitted = false
          try{
              this.form['user_id'] = 0
              let response = await create_transaction_record(this.form)
              this.showAlert = "true"
              this.alertMessage = "create sucess"
              this.alertType = 'success'
          }
          catch (error){
              this.showAlert = "true"
              this.alertMessage = "create error"
              this.alertType = 'error'
          }
        }
    },
  },
  mounted() {
    this.form.date = this.getTodayDate();
    this.timer = setInterval(() => {
      this.form.date = this.getTodayDate();
    }, 1000);
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
}
</script>

<style scoped>
.transaction-container{
  display: grid;
  place-items: center;
  width: 20vw;
  z-index: 1;
}
.v-form {
  position: relative;
  width: 20vw;
  margin: auto;
  z-index: 1;
}
.alert{
    position: fixed;
    place-items: center;
    z-index: 2;
  }
</style>
