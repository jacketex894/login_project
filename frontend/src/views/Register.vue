<template>
    <div class = "register-container">
        <v-sheet :elevation="24" rounded class = "register-title">
            <h2> Register </h2>
        </v-sheet>
        <v-sheet :elevation="24" rounded class = "register-sheet">
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
                <v-text-field
                    v-model="mail"
                    :rules="[value => required(value, 'Email')]"
                    label="Email Address"
                ></v-text-field>
                <v-btn class="submitButton" type="submit" block v-on:click="userRegister()">Submit</v-btn>
            </v-form>
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
import {register} from '@/utils/userProfile.js'
export default {
    name: 'Register',
    data(){
        return{
            userName:null,
            mail:null,
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
        async userRegister(){
            let userData = {
                'user_name':this.userName,
                'mail':this.mail,
                'password':this.password
            };
            try{
                let response = await register(userData);
                this.showAlert = "true"
                this.alertMessage = "Register sucess"
                this.alertType = 'success'
                this.$router.push("/")
            }
            catch (error){
                this.showAlert = "true"
                this.alertMessage = "Register fail : The user name or email  is duplicated, please check."
                this.alertType = 'error'
            }
        }
    }
}
</script>

<style scoped>
  .register-container {
    display: grid;
    place-items: center;
    height: 50vh;
    z-index: 1;
  }
  .register-title{
    height: 5vh;
    width: 10vw;
    display: grid;
    place-items: center;
    background-color: rgba(240, 248, 255, 0.226);
    color: rgb(16, 26, 2)
  }
  .register-sheet{
    height: 40vh;
    width: 20vw;
    background-color: rgba(240, 248, 255, 0.84);
    padding: 20px; 
  }
  .alert{
    position: fixed;
    place-items: center;
    z-index: 2;
  }
  .submitButton{
  }
</style>
