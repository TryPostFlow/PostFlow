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
                                    <a v-for="tag_item in tags" track-by="id" class="list-group-item clearfix b-l-3x" v-bind:class="$route.params.tag_id == tag_item.id?'b-l-info':''" v-link="{ name: 'TagEdit', params: { tag_id: tag_item.slug }}">
                                        {{tag_item.name}} <span class="label label-default">{{tag_item.slug}}</span>
                                    </a>
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
    import {API} from '../api.js'
    let $ = require('jQuery')
    export default{
        name: 'TagList',
        data () {
            return {
                tag: {},
                tags: [],
                p: 1
            }
        },
        route: {
            data ({ to }) {
                var resource = this.$resource(API.TAG)
                resource.query({p: this.p}).then(function(response){
                    this.tags = this.tags.length?this.tags:response.data
                    if (this.$route.name == 'TagList') {
                        if (this.tags.length > 0) {
                            this.$route.router.go(
                                {
                                    name: 'TagEdit',
                                    params: { tag_id: this.tags[0].slug }
                                }
                            )
                        }
                    };
                })
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
                   let resource = this.$resource(API.TAG)
                   this.p += 1
                    resource.query({p: this.p}).then(function(response){
                        this.tags = this.tags.concat(response.data)
                        lock = false
                    })
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