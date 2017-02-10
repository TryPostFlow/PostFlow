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
            <ui-editor v-model="post" ></ui-editor>
        </div>
    </div>
    <div class="app-footer wrapper b-t bg-light">
        <div class="form-horizontal">
            <div class="form-group" style="margin-bottom: 0;">
                <label for="tags" class="control-label col-lg-1">Tags</label>
                <div class="col-lg-10">
                    <ui-select multiple="multiple" :tags=true v-model="post.tags"></ui-select>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
    import toastr from 'toastr'
    import editor from '../components/Editor.vue'
    import select from '../components/Select.vue'
    import DropdownButton from '../components/DropdownButton.vue'

    export default{
        name: 'PostsCreate',
        data () {
            return {
                post:{
                    markdown:'',
                    content:'',
                    tags:[]
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
                this.$store.dispatch(
                'post/CREATE_ITEM',
                {
                    path: `posts`,
                    params: this.post
                }).then((response)=>{
                    toastr.options.positionClass = 'toast-bottom-right';
                    toastr.success('Save successfully.', {timeOut: 3000})
                    this.$router.push({name:'PostEdit', params:{post_id: response.data.id}})
                }, (error) => {
                    console.error(error)
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