<template>
<div class="col">
    <div class="wrapper b-b clear">
        <h2 class="font-thin m-n pull-left">{{post.title}}</h2>
        <a v-link="{ name: 'PostEdit', params: { post_id: post.id }}" class="btn btn-default btn-sm pull-right">Edit</a>
    </div>
    <div class="wrapper">{{{post.content}}}</div>
</div>
</template>
<script>
import {API} from '../api.js'

export default{
    name: 'PostView',
    data () {
        return {
            post: {},
            posts: []
        }
    },
    route: {
        data ({ to }) {
            var resource = this.$resource(API.POST)
            resource.get({id: to.params.post_id}).then(function(response){
                this.post = response.data
            })
        }
    }
}
</script>
<style>

</style>