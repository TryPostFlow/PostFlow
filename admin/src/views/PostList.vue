<template>
    <div class="app-content">
      <div class="app-content-body">

<div class="hbox hbox-auto-xs hbox-auto-sm">
    <div class="col w-xl bg-light dk b-r bg-auto">
        <ul class="list-group list-group-lg no-radius m-b-none m-t-n-xxs">
            <li v-for="post_item in posts" track-by="id" class="list-group-item clearfix b-l-3x" v-bind:class="$route.params.post_id == post_item.id?'b-l-info':''">
                <div>
                    <a class="text-md" v-link="{ name: 'PostView', params: { post_id: post_item.id }}">{{post_item.title}}</a>
                </div>
                <div class="text-ellipsis m-t-xs"><span class="label bg-light m-l-sm" v-for="tag in post_item.tags">{{tag.name}}</span></div>
            </li>
        </ul>
    </div>
    <router-view></router-view>
</div>

</div>
</div>



</template>

<script>
    import {API} from '../api.js'

    export default{
        name: 'PostList',
        data () {
            return {
                post: {},
                posts: []
            }
        },
        route: {
            data ({ to }) {
                var resource = this.$resource(API.POST)
                resource.query().then(function(response){
                    this.posts = response.data
                    if (this.$route.name == 'PostList') {
                        if (this.posts.length > 0) {
                            this.$route.router.go(
                                {
                                    name: 'PostView',
                                    params: { post_id: this.posts[0].id }
                                }
                            )
                        }
                    };
                })
            }
        }
    }
</script>
<style>
    .list-group-item:first-child{
        border-top-left-radius: 0;
        border-top-right-radius: 0;
    }
    .list-group-item:last-child{
        border-bottom-right-radius: 0;
        border-bottom-left-radius: 0;
    }
</style>