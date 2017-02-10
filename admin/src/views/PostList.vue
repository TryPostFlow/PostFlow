<template>
<div class="app-content h-full">
    <div class="app-content-body app-content-full h-full">
        <div class="hbox hbox-auto-xs hbox-auto-sm">
            <div class="col w-xl bg-light dk b-r bg-auto">
                <div class="vbox">
                    <div class="row-row">
                        <div class="cell scrollable hover" @scroll="loadmore">
                            <div class="cell-inner">
                                 <ul class="list-group list-group-lg no-radius m-b-none m-t-n-xxs">
                                    <li v-for="post_item in posts" :key="post_item.id" class="list-group-item clearfix b-l-3x" v-bind:class="$route.params.post_id == post_item.id?'b-l-info':''">
                                        <div>
                                            <router-link class="text-md" :to="{ name: 'PostView', params: { post_id: post_item.id }}">{{post_item.title}}</router-link>
                                        </div>
                                        <div class="text-ellipsis m-t-xs"><span class="label bg-light m-l-sm" v-for="tag in post_item.tags">{{tag.name}}</span></div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <router-view></router-view>
        </div>
    </div>
</div>
</template>
<script>
const $ = require('jQuery')
function fetchPosts(store, page){
    let params = {
        p: page?page:1
    }
    return store.dispatch('post/FETCH_ITEMS', {path: 'posts', params:params})
}
export default{
    name: 'PostList',
    computed: {
        posts(){
            return this.$store.getters['post/GET_ITEMS']().data
        },
        page(){return this.$store.getters['post/GET_ITEMS']().page}
    },
    methods:{
        loadmore: function(e){
            let lock = false;
            if($(e.target).scrollTop() - $('.app-header').height() +1 == $('.scrollable .list-group').height() - $(window).height() && !lock)
            {
                  // load your content
                console.log('bottom')
                lock = true;
                fetchPosts(this.$store, this.page+1).then(()=>{lock=false})
            }
        }
    },
    watch:{
        '$route':function(){
            if (this.$route.name == 'PostList'){
                fetchPosts(this.$store).then(()=>{
                    if(this.posts.length > 0){
                        this.$router.push({name: 'PostView', params: { post_id: this.posts[0].id }})
                    }
                })
            }
        }
    },
    beforeMount(){
        fetchPosts(this.$store).then(()=>{
             if (this.$route.name == 'PostList' && this.posts.length > 0){
                this.$router.push({name: 'PostView', params: { post_id: this.posts[0].id }})
            }
        })
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