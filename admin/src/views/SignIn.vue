<template>
<el-row type="flex" class="row" justify="center">
  <el-col :span="6">
  <a href class="navbar-brand block m-t">{{app.name}}</a>
  <div class="m-b-lg">
    <el-form :model="user">
      <div class="text-danger wrapper text-center" v-show="authError">
          {{authError}}
      </div>
      <!-- <div class="list-group list-group-sm"> -->
        <el-form-item>
          <el-input v-model="user.username" placeholder="Email" required></el-input>
        </el-form-item>
        <el-form-item>
           <el-input type="password" placeholder="Password" v-model="user.password" required></el-input>
        </el-form-item>
      <!-- </div> -->
      <el-button type="primary" @click="signin()" class="btn-block" size="large">Log in</el-button>
    </el-form>
  </div>
  </el-col>
</el-row>
</template>
<script>
import axios from '../store/constants/api'
var qs = require('qs');
export default{
  data() {
    return {
      app: this.$parent.app,
      user: {
        grant_type: 'password',
        client_id: 'J1SuWr9nNV618NgJ4kZPM4DvYVY68AjtxDRsokZI',
        client_secret: 'bM17VfEkCAmmcMTm81g0VExTsPPDSVzTDbCZZKoEDQZdZqTm05'
      },
      authError: null
    }
  },
  methods: {
    signin(){
      axios.post(
        'auth/token',
        qs.stringify(this.user),
        {
          headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        })
      .then(function (response) {
        localStorage.setItem('auth', JSON.stringify(response.data))
        this.$router.push({name: 'PostList'})
      })
      // .catch(function(error){
      //   this.authError = error
      // })
      
    }
  }
  // beforeMount(){
  //     if (this.$root.isLogin) {
  //       this.$route.router.replace({name: 'PostList'})
  //     };
  // }
}
</script>
<style>
.navbar-brand{
  // display: inline-block;
  height: auto;
  font-size: 20px;
  font-weight: 700;
  line-height: 50px;
  text-align: center;
  float: none;
  padding: 0px 20px;
}
.navbar-brand:hover{
  text-decoration: none;
}

</style>