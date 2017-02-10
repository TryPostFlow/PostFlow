<template>
    <div class="aside" v-show="isActive" @click.self="handleClose">
        <div class="modal-card bg-white-only b-l">
            <div class="wrapper b-b">
               <strong>{{title}}</strong> <a href="javascript:void(0)" @click="handleClose"><i class="fa fa-close"></i></a>
            </div>
            <div class="wrapper">
                <slot></slot>
            </div>
        </div>
    </div>
</template>
<script>
    export default{
        name: 'Aside',
        props: {
            title:{
                type: String
            },
            isShow: {
                type: Boolean,
                default: false
            }
        },
        data(){
            return{
                isActive: false
            }
        },
        watch: {
            isShow(val){
                this.isActive = val;
            }
        },
        methods:{
            handleClose(){
                this.$emit('close')
            },
            handleCancle(){
                console.log('cancle')
            }
        }
    }
</script>
<style>
    .aside {
        position: fixed;
        z-index: 1986;
        bottom: 0;
        left: 0;
        right: 0;
        top: 0;
        transition: all .3s ease;
    }
    .aside .modal-card{
        width: 450px;
        max-width: 100%;
        margin: 0;
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        max-height: 100%;
        border-radius: 0;
    }
    .aside.aside-right .modal-card{
        left: auto;
        right: 0;
    }
    .aside.aside-right .fa-close{
        float: right;
        font-size: 18px;
    }
</style>