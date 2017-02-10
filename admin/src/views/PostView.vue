<template>
<div class="col">
    <div class="vbox">
        <div class="row-row">
            <div class="cell">
                <div class="cell-inner">
                    <div class="wrapper b-b clear">
                        <h2 class="font-thin m-n pull-left">{{post.title}}</h2>
                        <a href="javascript:void(0)" class="btn btn-danger btn-sm pull-right" @click="isShow=true"><i class="fa fa-trash"></i></a>
                        <router-link :to="{ name: 'PostEdit', params: { post_id: post.id }}" class="btn btn-default btn-sm btn-addon pull-right m-r-xs">
                            <i class="fa fa-pencil"></i> Edit
                        </router-link>
                        <modal title="Delete Post" :is-show="isShow" @close="isShow=false" :on-ok="remove">
                            Are you sure?
                        </modal>
                    </div>
                    <div class="wrapper" v-html="post.content"></div>
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
    name: 'PostView',
    data(){
        return{
            isShow: false
        }
    },
    computed:{
        post(){
            return this.$store.getters['post/GET_ITEM'](this.$store.state.route.params.post_id) || {}
        }
    },
    methods:{
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
        }
    },
    beforeMount(){
        fetchPost(this.$store)
    },
    components:{
        Modal
    }
}
</script>
<style>

</style>