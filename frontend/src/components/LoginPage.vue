<template>
    <div>
        <h2> Login </h2>
        <div>
            <label> Account </label>
            <input v-model="account"/>
        </div>
        <div>
            <label> Password </label>
            <input v-model="password"/>
        </div> 
    </div>
    <button v-on:click="test()"> Login </button>
</template>
<script>

import {login} from '@/utils/login.js'
export default {
    data(){
        return{
            account:null,
            password:null,
        };
    },
    methods:{
        test(){
            login(this.account,this.password)
        }
    }
}
</script>