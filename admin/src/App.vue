<template>
  <div class="app" v-bind:class="{'app-header-fixed':app.settings.headerFixed, 'app-aside-fixed':app.settings.asideFixed, 'app-aside-folded':app.settings.asideFolded, 'app-aside-dock':app.settings.asideDock, 'container':app.settings.container}">
    <div class="app-header navbar" v-if="$route.meta.auth">
        <div class="navbar-header bg-black">
          <a href="#/" class="navbar-brand text-lt">
            <i class="fa fa-globe"></i>
            <span class="hidden-folded m-l-xs ng-binding">{{app.name}}</span>
          </a>
        </div>
        <div class="collapse pos-rlt navbar-collapse box-shadow bg-white-only">
            <div class="nav navbar-nav hidden-xs">
              <a href="#" class="btn no-shadow navbar-btn">
                <i class="fa fa-fw fa-dedent"></i>
              </a>
            </div>
            <ul class="nav navbar-nav navbar-right">
              <li>
                    <router-link :to="{name: 'SignOut'}">Sign Out</a>
                  </li>
            </ul>
        </div>
    </div>
    <div class="app-aside hidden-xs bg-black" v-if="$route.meta.auth">
        <div class="aside-wrap">
          <div class="navi-wrap">
            <nav class="navi clearfix">
              <ul class="nav">
                <li v-bind:class="$route.name == 'PostCreate'?'active':''">
                  <router-link :to="{ name: 'PostCreate'}">
                    <i class="fa fa-pencil-square-o"></i>
                    <span class="font-bold">New Post</span>
                  </router-link>
                </li>
                <li v-bind:class="$route.name == 'PostList' || $route.name == 'PostView' || $route.name == 'PostEdit'?'active':''">
                  <router-link :to="{ name: 'PostList'}">
                    <i class="fa fa-list"></i>
                    <span class="font-bold">Posts</span>
                  </router-link>
                </li>
                <li v-bind:class="$route.name == 'TagList' || $route.name == 'TagView' || $route.name == 'TagEdit'?'active':''">
                  <router-link :to="{ name: 'TagList'}">
                    <i class="fa fa-tag"></i>
                    <span class="font-bold">Tags</span>
                  </router-link>
                </li>
              </ul>
            </nav>
          </div>
        </div>
    </div>

    <router-view keep-alive transition-mode="out-in">
    </router-view>

  </div>
</template>
<script>

  import {API} from './api.js'
  export default{
    data() {
      return {
        app: {
          name: 'Planet',
          version: '0.0.1',
          settings: {
            themeID: 1,
            navbarHeaderColor: 'bg-black',
            navbarCollapseColor: 'bg-white-only',
            asideColor: 'bg-black',
            headerFixed: true,
            asideFixed: true,
            asideFolded: false,
            asideDock: false,
            container: false
          }
        },
        account: {},
        auth: localStorage.getItem('auth')?JSON.parse(localStorage.getItem('auth')):null
      }
    },
    methods:{
      signout:function(){
            localStorage.removeItem('auth')
            this.isLogin = false
            this.$route.router.go({name: 'SignIn'})
        }
    }
  }
</script>
<style>
</style>