<template>
    <div class = "login-container">
        <v-sheet :elevation="24" rounded class = "login-title">
            <h2> Login </h2>
        </v-sheet>
        <v-sheet :elevation="24" rounded class = "login-sheet">
            <v-form @submit.prevent>
                <v-text-field
                    v-model="userName"
                    :rules="[value => required(value, 'User Name')]"
                    label="User Name"
                ></v-text-field>
                <v-text-field
                    v-model="password"
                    :rules="[value => required(value, 'Password')]"
                    label="Password"
                ></v-text-field>
                <v-btn  class = "submitButton" type="submit" block v-on:click="userLogin()">Submit</v-btn>
            </v-form>
            <p><router-link to="/register">Go to Register Page</router-link></p>
        </v-sheet>
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
    </div>
</template>
<script>

import {login} from '@/utils/userProfile.js'
export default {
    name: 'Login',
    data(){
        return{
            userName:null,
            password:null,
            showAlert:false,
            alertMessage:null,
            alertType:null,
        };
    },
    methods:{
        required(value, fieldName) {
            if (value) return true;
                return `You must enter a ${fieldName}.`;
        },
        async userLogin(){
            let userData = {
                'user_name':this.userName,
                'password':this.password
            };
            try{
                let response = await login(userData);
                this.showAlert = "true"
                this.alertMessage = "Login sucess"
                this.alertType = 'success'
                router.push("/expense")
            }
            catch (error){
                this.showAlert = "true"
                this.alertMessage = "Login fail : The user name or password  is wrong, please check."
                this.alertType = 'error'
            }
        }
    }
}
</script>

<style scoped>
  .login-container {
    display: grid;
    place-items: center;
    height: 50vh;
    z-index: 1;
  }
  .login-title{
    height: 5vh;
    width: 10vw;
    display: grid;
    place-items: center;
    background-color: rgba(240, 248, 255, 0.226);
    color: rgb(16, 26, 2)
  }
  .login-sheet{
    height: 40vh;
    width: 20vw;
    background-color: rgba(240, 255, 245, 0.84);
    padding: 20px; 
  }
  .alert{
    position: fixed;
    place-items: center;
    z-index: 2;
  }
  .submitButton{
    top:10vh;
  }
</style>
