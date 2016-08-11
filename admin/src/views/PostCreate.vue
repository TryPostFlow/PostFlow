<template>
    <div class="app-content">
      <div class="app-content-body">

<div class="wrapper-sm b-b clearfix">
        <div class="pull-left">
            <input class="form-control input-lg no-radius no-border no-bg text-lg" type="text" v-model="post.title" placeholder="Post title">
        </div>
        <div class="pull-right">
        <ui-dropdown-button :items='buttons' @action="save"></ui-dropdown-button>
        </div>
</div>
<div class="app-content-full h-full" style="top: 117px; bottom:50px;">
    <ui-editor :markdown.sync="post.markdown" :content.sync="post.content"></ui-editor>
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
    import {API} from '../api.js'
    import toastr from 'toastr'
    import editor from '../components/Editor.vue'
    import select from '../components/Select.vue'
    import DropdownButton from '../components/DropdownButton.vue'
    import jQuery from 'jquery'
    window.jQuery = jQuery
    require('bootstrap/js/dropdown.js')

    export default{
        name: 'PostsCreate',
        data () {
            return {
                post: {
                    markdown: '',
                    tags: []
                },
                buttons: [
                    {
                        dataTarget: 'draft',
                        text: 'Save Draft'
                    },
                    {
                        dataTarget: 'published',
                        text: 'Publish Now'
                    }
                ]
            }
        },
        methods: {
            save: function (status) {
                this.post.status = status
                var resource = this.$resource(API.POST)
                resource.save(this.post).then(function(response){
                    this.post = {markdown: '', tags:[]}
                    toastr.options.positionClass = 'toast-bottom-right';
                    toastr.success('Save successfully.', {timeOut: 3000})
                    this.$route.router.go({name:'PostEdit', params:{post_id: response.data.id}})
                })
            }
        },
        components: {
            'ui-select': select,
            'ui-editor': editor,
            'ui-dropdown-button': DropdownButton
        }
    }
</script>
<style>

</style>