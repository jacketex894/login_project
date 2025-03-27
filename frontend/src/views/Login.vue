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
    <button v-on:click="show()"> Login </button>
    <p><router-link to="/register">Go to Register Page</router-link></p>
</template>
<script>

import {login} from '@/utils/userDB.js'
export default {
    name: 'Login',
    data(){
        return{
            account:null,
            password:null,
        };
    },
    methods:{
        show(){
            login(this.account,this.password)
        }
    }
}
</script>