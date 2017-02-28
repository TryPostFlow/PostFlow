<template>
<div class="container w-xxl w-auto-xs">
  <a href class="navbar-brand block m-t">{{app.name}}</a>
  <div class="m-b-lg">
    <div class="wrapper text-center">
      <strong>Sign in to get in touch</strong>
    </div>
    <form name="form" class="form-validation" @submit.prevent="signin">
      <div class="text-danger wrapper text-center" v-show="authError">
          {{authError}}
      </div>
      <div class="list-group list-group-sm">
        <div class="list-group-item">
          <input type="email" placeholder="Email" class="form-control no-border" v-model="user.email" required>
        </div>
        <div class="list-group-item">
           <input type="password" placeholder="Password" class="form-control no-border" v-model="user.password" required>
        </div>
      </div>
      <button type="submit" class="btn btn-lg btn-primary btn-block" @click.stop.prevent="signin">Log in</button>
      <div class="text-center m-t m-b"><a href="javascript:void(0)">Forgot password?</a></div>
      <div class="line line-dashed"></div>
      <p class="text-center"><small>Do not have an account?</small></p>
      <a href="javascript:void(0)" class="btn btn-lg btn-default btn-block">Create an account</a>
    </form>
  </div>
  <div class="text-center">
    <p>
      <small class="text-muted">Web app framework base on VueJS<br>&copy; 2017</small>
    </p>
  </div>
</div>
</template>
<script>
import axios from '../store/constants/api'
var qs = require('qs');
export default{
  data() {
    return {
      app: this.$parent.app,
      user: {
//        grant_type: 'password',
//        client_id: 'J1SuWr9nNV618NgJ4kZPM4DvYVY68AjtxDRsokZI',
//        client_secret: 'bM17VfEkCAmmcMTm81g0VExTsPPDSVzTDbCZZKoEDQZdZqTm05'
      },
      authError: null
    }
  },
  methods: {
    signin(){
      var vm = this
      axios.post(
        'login',
        this.user)
      .then(function (response) {
        localStorage.setItem('auth', JSON.stringify(response.data))
        vm.$router.push({name: 'PostList'})
      })
      .catch(function(error){
        if (error.response) {
          vm.authError = error.response.data.error
          console.log(error.response.data);
          console.log(error.response.status);
          console.log(error.response.headers);
        } else {
          // Something happened in setting up the request that triggered an Error
          console.log('Error', error.message);
        }
        console.log(error.config);
      })
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