<template>
    <div class="app-content">
      <div class="app-content-body">

<div class="wrapper-sm b-b">
    <div class="row">
        <div class="col-lg-11">
            <input class="form-control input-lg no-radius no-border no-bg text-lg" type="text" v-model="post.title">
        </div>
        <div class="col-lg-1">
             <a @click="update" class="btn btn-primary">Save</a>
        </div>
    </div>
</div>
<div class="app-content-full h-full" style="top: 117px; bottom:50px;">
    <ui-editor :markdown.sync="post.markdown"></ui-editor>
</div>

</div>
</div>

<div class="app-footer wrapper b-t bg-light">
    <div class="form-horizontal">
        <div class="form-group" style="margin-bottom: 0;">
            <label for="tags" class="control-label col-lg-1">Tags</label>
            <div class="col-lg-10">
                <ui-select multiple="multiple" :tags=true :selected.sync="post.tags"></ui-select>
            </div>
        </div>
    </div>
</div>

</template>

<script>
    import {API} from '../../api.js'
    import toastr from 'toastr'
    import editor from './editor.vue'
    import select from './select.vue'

    export default{
        name: 'PostsEdit',
        data () {
            return {
                post: {
                    markdown: '',
                    tags: []
                }
            }
        },
        route: {
            data ({ to }) {
                var resource = this.$resource(API.POST)
                resource.get({id: to.params.post_id}).then(function(response){
                    this.post = response.data
                })
            }
        },
        methods: {
            update: function () {
                    var resource = this.$resource(API.POST)
                    resource.update(
                        {id: this.$route.params.post_id},
                        this.post)
                    .then(function(response){
                        this.post = response.data
                        toastr.options.positionClass = 'toast-bottom-right';
                        toastr.success('Save successfully.', {timeOut: 3000})
                    })
            }
        },
        components: {
            'ui-select': select,
            'ui-editor': editor
        }
    }
</script>
<style>
    @import "toastr";
</style>