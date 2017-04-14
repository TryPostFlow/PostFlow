<template>
<div class="app-content">
    <div class="app-content-body">
        <div class="bg-light lter b-b wrapper-md clearfix">
            <h1 class="m-n font-thin h3 pull-left">Settings</h1>
            <a href="javascript:void(0)" class="btn btn-primary pull-right" @click="save">Save</a>
        </div>
        <div class="wrapper-md">
            <form class="form-horizontal">
                <div class="form-group">
                    <label class="col-lg-2 control-label">Blog Title</label>
                    <div class="col-lg-10">
                        <input type="text" class="form-control" v-model="settings.title.value">
                        <span class="help-block m-b-none">The name of your blog</span>
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-lg-2 control-label">Blog Description</label>
                    <div class="col-lg-10">
                        <textarea name="" id="" cols="30" rows="5" class="form-control" v-model="settings.description.value"></textarea>
                        <span class="help-block m-b-none">The name of your blog</span>
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-lg-2 control-label">Blog Logo</label>
                    <div class="col-lg-10">
                        <dropzone :image_url="settings.logo.value" @success="successLogoHandler" @remove="removeLogoHandler"></dropzone>
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-lg-2 control-label">Blog Cover</label>
                    <div class="col-lg-10">
                        <dropzone :image_url="settings.cover.value" @success="successCoverHandler" @remove="removeCoverHandler"></dropzone>
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-lg-2 control-label">Posts per page</label>
                    <div class="col-lg-10">
                        <input type="text" class="form-control" v-model="settings.postsPerPage.value">
                        <span class="help-block m-b-none">How many posts should be displayed on each page</span>
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-lg-2 control-label">Google Analytics Tracking ID</label>
                    <div class="col-lg-10">
                        <input type="text" class="form-control" v-model="settings.ga_id.value">
                        <span class="help-block m-b-none">The tracking ID of Google Analytics</span>
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-lg-2 control-label">Disqus ID</label>
                    <div class="col-lg-10">
                        <input type="text" class="form-control" v-model="settings.disqus_id.value">
                        <span class="help-block m-b-none">The shortname of your blog in the Disqus</span>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
</template>
<script>
import toastr from 'toastr'
import 'toastr/build/toastr.css'
import Dropzone from '../components/Dropzone.vue'

function fetchSettings(store){
    return store.dispatch('setting/FETCH_ITEMS', {path: 'settings', index:'key'})
}

export default{
    name: 'Settings',
    computed: {
        settings(){
            return this.$store.state.Setting.data
        }
    },
    methods:{
        save(){
            this.$store.dispatch(
            'setting/UPDATE_ITEM',
            {
                path: `settings`,
                params: this.settings,
                index: 'key'
            }).then(()=>{
                toastr.options.positionClass = 'toast-bottom-right';
                toastr.success('Save successfully.', {timeOut: 3000})
            })
        },
        successLogoHandler(file, response){
            this.$set(this.settings.logo, 'value', response.url)
        },
        removeLogoHandler(path){
            this.settings.logo.value = ''
        },
        successCoverHandler(file, response){
            this.$set(this.settings.cover, 'value', response.url)
        },
        removeCoverHandler(path){
            this.settings.cover.value = ''
        }
    },
    beforeMount(){
        fetchSettings(this.$store)
    },
    components:{
        Dropzone
    }
}
</script>
<style>
.image-container {
    text-align: center;
    display: table-cell;
}
</style>