<template>
<div class="col w-xxl">
    <div class="vbox">
        <div class="row-row">
            <div class="cell">
                <div class="cell-inner">
                    <div class="wrapper b-b">
                        <router-link :to="{ name: 'TagCreate'}" class="btn btn-sm btn-default">New TAG</router-link>
                    </div>
                    <div class="wrapper b-b clear">
                        <div class="font-bold m-b">Tag Settings</div>
                        <form role="form" v-on:submit.prevent>
                            <div class="form-group">
                                <dropzone :image_url="tag.image" @success="successhandler" @remove="removehandler"></dropzone>
                            </div>
                            <div class="form-group">
                                <label>Name</label>
                                <input type="text" class="form-control" v-model="tag.name" @blur="save">
                            </div>
                            <div class="form-group">
                                <label>URL</label>
                                <input type="text" class="form-control" v-model="tag.slug">
                            </div>
                            <div class="form-group">
                                <label>Description</label>
                                <textarea class="form-control" name="description" id="description" cols="30" rows="10" v-model="tag.description"></textarea>
                            </div>
                            <div class="form-group">
                                <button type="submit" class="btn btn-sm btn-success pull-left" @click="save"><i class="fa fa-save"></i> SAVE TAG</button>
                                <button type="submit" class="btn btn-sm btn-link text-danger pull-right" @click="remove"><i class="fa fa-trash"></i> DELETE TAG</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

    </div>
</div>
</template>
<script>
import toastr from 'toastr'
import 'toastr/build/toastr.css'

import Dropzone from '../components/Dropzone.vue'

function fetchTag(store){
    return store.dispatch(
        'tag/FETCH_ITEM',
        {
            path: `tags/${store.state.route.params.tag_id}`,
            params: {
                id: store.state.route.params.tag_id
            }
        })
}

export default{
    name: 'TagEdit',
    computed:{
        tag(){
            return this.$store.getters['tag/GET_ITEM'](this.$store.state.route.params.tag_id) || {}
        }
    },
    methods: {
        save: function(){
            this.$store.dispatch(
                'tag/UPDATE_ITEM',
                {
                    path: `tags/${this.$store.state.route.params.tag_id}`,
                    params: this.tag
                })
                .then(()=>{
                    toastr.options.positionClass = 'toast-bottom-right';
                    toastr.success('Save successfully.', {timeOut: 3000})
                })
        },
        remove(){
            this.$store.dispatch(
                'tag/DELETE_ITEM',
                {
                    path: `tags/${this.$store.state.route.params.tag_id}`,
                    params:{
                        key: this.$store.state.route.params.tag_id
                    }
                })
                .then(()=>{
                    toastr.options.positionClass = 'toast-bottom-right';
                    toastr.success('Delete successfully.', {timeOut: 3000})
                     this.$router.push({name:'TagList'})
                })
        },
        successhandler(file, response){
            this.tag.image = response.url
            this.tag._image = response.filename
        },
        removehandler(path){
            this.tag.image = null
            this.tag._image = null
        }
    },
    beforeMount(){
        fetchTag(this.$store)
    },
    components:{
        Dropzone
    }
}
</script>
<style>

</style>