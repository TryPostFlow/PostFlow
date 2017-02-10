<template>
<div class="app-content">
    <div class="app-content-body">
        <div class="wrapper-sm b-b clearfix">
            <div class="pull-left">
                <input class="form-control input-lg no-radius no-border no-bg text-lg" type="text" v-model="post.title">
            </div>
            <div class="pull-right">
                 <ui-dropdown-button :items='buttons' @action="update"></ui-dropdown-button>
                 <modal title="Delete Post" :is-show="isDeleteShow" @close="isDeleteShow=false" :on-ok="remove">
                    Are you sure?
                </modal>
                 <a class="btn btn-default" href="javascript:void(0)" @click="isShow=true"><i class="fa fa-gear"></i></a>
            </div>
        </div>
        <div class="app-content-full h-full" style="top: 117px; bottom:50px;">
            <ui-editor v-model="post"></ui-editor>
            <ui-aside class="aside-right" title="Post Settings" :is-show="isShow" @close="isShow=false">
                <form>
                    <div class="form-group">
                        <label>Post URL</label>
                        <div class="input-group">
                            <span class="input-group-addon"><i class="fa fa-link"></i></span>
                            <input type="text" class="form-control" v-model="post.slug">
                        </div>
                    </div>
                </form>
            </ui-aside>
        </div>
    </div>
    <div class="app-footer wrapper b-t bg-light">
        <div class="form-horizontal">
            <div class="form-group" style="margin-bottom: 0;">
                <label for="tags" class="control-label col-lg-1">Tags</label>
                <div class="col-lg-10">
                    <!-- <ui-select multiple="multiple" :tags=true v-model="post.tags"></ui-select> -->
                    <v-select
                        v-model="tags"
                        multiple
                        :taggable="true"
                        max-height='200px'
                        :on-search="getOptions"
                        :options="options">
                    </v-select>
                </div>
            </div>
        </div>
    </div>
</div>
</template>
<script>
    import toastr from 'toastr'
    import 'toastr/build/toastr.css'
    import Modal from '../components/Modal.vue'
    import editor from '../components/Editor.vue'
    import select from '../components/Select.vue'
    import vSelect from '../components/vue-select'
    import DropdownButton from '../components/DropdownButton.vue'
    import Aside from '../components/Aside.vue'
    import '../css/yue.css'
    

    function fetchPost(store){
        return store.dispatch(
            'post/FETCH_ITEM',
            {
                path: `posts/${store.state.route.params.post_id}`,
                params: {
                    id: store.state.route.params.post_id
                }
            })
    }

    export default{
        name: 'PostsEdit',
        data(){
            return {
                isShow: false,
                isDeleteShow:false,
                options:[],
                tags:[]
            }
        },
        computed: {
            buttons: function(){
                if (this.post.status == 'draft') {
                    return [
                        {
                            dataTarget: 'draft',
                            text: 'Save Draft'
                        },
                        {
                            dataTarget: 'published',
                            text: 'Publish Now'
                        },
                        {
                            dataTarget: 'delete',
                            text: 'Delete Post'
                        }
                    ]
                }
                return [
                    {
                        dataTarget: 'published',
                        text: 'Update Post'
                    },
                    {
                        dataTarget: 'draft',
                        text: 'Unpublish'
                    },
                    {
                        dataTarget: 'delete',
                        text: 'Delete Post'
                    }
                ]
            },
            post(){
                return this.$store.getters['post/GET_ITEM'](this.$store.state.route.params.post_id) || {}
            }
        },
        methods: {
            update: function (status) {
                if(status === 'delete'){
                    this.isDeleteShow = true
                }
                else{
                    this.post.status = status
                    this.$store.dispatch(
                    'post/UPDATE_ITEM',
                    {
                        path: `posts/${this.$store.state.route.params.post_id}`,
                        params: this.post
                    }).then(()=>{
                        toastr.options.positionClass = 'toast-bottom-right';
                        toastr.success('Save successfully.', {timeOut: 3000})
                    })
                }
            },
            remove(){
                this.$store.dispatch(
                'post/DELETE_ITEM',
                {
                    path: `posts/${this.$store.state.route.params.post_id}`,
                    params:{
                        key: this.$store.state.route.params.post_id
                    }
                }).then(()=>{
                    toastr.options.positionClass = 'toast-bottom-right';
                    toastr.success('Delete successfully.', {timeOut: 3000})
                    this.$router.push({name:'PostList'})
                })
            },
            getOptions(search, loading) {
                loading(true)
                this.$store.dispatch(
                'tag/FETCH_ITEMS',
                {
                    path: `tags`,
                    params: {
                        q: search,
                        limit: 10
                    },
                    request: 'search'
                }).then(()=>{
                    this.options = []
                    this.$store.getters['tag/GET_ITEMS']('search').data.forEach(
                        item =>{
                            this.options.push({label:item.name, value:item.id})
                        }
                    )
                     loading(false)
                })
              }
        },
        beforeMount(){
            fetchPost(this.$store).then(()=>{
                this.post.tags.forEach(item =>{
                    this.tags.push({label:item.name, value: item.id})
                })
            })
        },
        components: {
            vSelect,
            Modal,
            // 'ui-select': select,
            'ui-editor': editor,
            'ui-dropdown-button': DropdownButton,
            'ui-aside': Aside
        }
    }
</script>
<style>
    /*@import "toastr";*/
</style>