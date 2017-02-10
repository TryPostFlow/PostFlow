<template>
<div class="app-content h-full">
    <div class="app-content-body app-content-full h-full">
        <div class="hbox hbox-auto-xs hbox-auto-sm">
            <div class="col bg-light dk b-r bg-auto">
                <div class="vbox">
                    <div class="row-row">
                        <div class="cell scrollable hover" @scroll="loadmore">
                            <div class="cell-inner">
                                 <div class="list-group list-group-lg no-radius m-b-none m-t-n-xxs">
                                    <router-link v-for="tag_item in tags" :key="tag_item.id" class="list-group-item clearfix b-l-3x" v-bind:class="$route.params.tag_id == tag_item.id?'b-l-info':''" :to="{ name: 'TagEdit', params: { tag_id: tag_item.id }}">
                                        {{tag_item.name}} <span class="label label-default">{{tag_item.slug}}</span>
                                    </router-link>
                                </div>
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

    function fetchTags(store, page){
        let params = {
            p: page?page:1
        }
        return store.dispatch('tag/FETCH_ITEMS', {path: 'tags', params:params})
    }

    export default{
        name: 'TagList',
        computed:{
            tags(){
                return this.$store.getters['tag/GET_ITEMS']().data
            },
            page(){return this.$store.getters['tag/GET_ITEMS']().page}
        },
        beforeMount(){
            fetchTags(this.$store).then(()=>{
                this.$router.push({name: 'TagEdit', params: { tag_id: this.tags[0].id }})
            })
        },
        watch:{
            '$route': function(){
                fetchTags(this.$store)
            }
        },
        methods:{
            loadmore: function(e){
                let lock = false;
                if($(e.target).scrollTop() - $('.app-header').height() +1 == $('.scrollable .list-group').height() - $(window).height() && !lock)
                {
                      // load your content
                    console.log('bottom')
                    lock = true;
                    fetchTags(this.$store, this.page+1).then(()=>{lock=false})
                }
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