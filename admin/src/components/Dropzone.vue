<template>
<div class="dropzone-container">
    <div class="dropzone b-a b-2x b-dashed wrapper-lg lter text-center" v-show="!image_url"></div>
    <div class="image-container bg-light" v-if="image_url">
        <img :src="image_url" class="b b-a wrapper-xs bg-white img-responsive">
        <a class="btn btn-danger btn-icon btn-sm" @click="handleRemove" href="javascript:void(0)"><i class="fa fa-trash"></i></a>
    </div>
</div>
</template>
<script>
    require('dropzone/dist/dropzone.css')
    export default{
        props:{
            image_url:{
                type: String,
                default: ''
            },
            upload_dir: String
        },
        data(){
            return {
                auth: JSON.parse(localStorage.getItem('auth'))
            }
        },
        mounted(){
          let self = this
          const url = "/images"
          var Dropzone = require("dropzone");
          Dropzone.autoDiscover = false;
          var element = this.$el.querySelector('div.dropzone')
          this.myDropzone = new Dropzone(
            element, 
            {
              url: url,
              headers:{
                'Authorization': 'Bearer ' + self.auth.access_token
              },
              maxFiles:1,
              success: function(file, response){
                  self.$emit('success', file, response)
              }
            });
        },
        methods:{
          handleRemove(){
            this.$emit('remove')
          }
        }
    }
</script>
<style>
.dropzone{
  cursor: pointer;
}
.image-container {
  position: relative;
}
.image-container img{
  display: block;
  width: 100%;
  height: 100%;
  min-height: 50px;
  vertical-align: middle;
}
.image-container .btn-icon{
  position: absolute;
  top: 5px;
  right: 5px;
}
</style>