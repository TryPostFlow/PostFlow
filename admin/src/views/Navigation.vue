<template>
<div class="app-content">
    <div class="app-content-body">
        <div class="bg-light lter b-b wrapper-md clearfix">
            <h1 class="m-n font-thin h3 pull-left">Navigation</h1>
            <a href="javascript:void(0)" class="btn btn-primary pull-right" @click="save">Save</a>
        </div>
        <div class="wrapper-md">
            <form class="form-horizontal" @submit.prevent="">
                <draggable @start="drag=true" @end="drag=false" v-model="navigations">
                    <div v-for="navigation, index in navigations" class="form-group">
                        <div class="col-md-5">
                            <div class="input-group">
                                <span class="input-group-btn outer">
                                    <button class="btn btn-primary btn-sm"><i class="fa fa-arrows-v"></i></button>
                                </span>
                                <input class="form-control" type="text" v-model="navigation.label">
                            </div>
                        </div>
                        <div class="col-md-7">
                            <div class="input-group">
                                <input class="form-control" type="text" v-model="navigation.url">
                                <span class="input-group-btn">
                                    <button class="btn btn-danger btn-sm" @click="removeNav(index)"><i class="fa fa-trash"></i></button>
                                </span>
                            </div>
                        </div>
                    </div>
                </draggable>
                <div class="form-group">
                    <div class="col-md-5">
                        <div class="input-group">
                            <span class="input-group-btn outer">
                                <button class="btn btn-link btn-sm"><i>&nbsp;&nbsp;</i></button>
                            </span>
                            <input class="form-control" type="text" v-model="nav.label">
                        </div>
                    </div>
                    <div class="col-md-7">
                        <div class="input-group">
                            <input class="form-control" type="text" v-model="nav.url">
                            <span class="input-group-btn">
                                <button class="btn btn-success btn-sm" @click="addNav"><i class="fa fa-plus"></i></button>
                            </span>
                        </div>
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
import Draggable from 'vuedraggable'

function fetchSettings(store){
    return store.dispatch('setting/FETCH_ITEMS', {path: 'settings', index:'key'})
}

export default{
    name: 'Settings',
    data(){
        return {
            nav:{}
        }
    },
    computed: {
        settings(){
            return this.$store.state.Setting.data
        },
        navigations:{
            get(){
                return JSON.parse(this.$store.state.Setting.data.navigation.value)
            },
            set(value){
                this.$store.state.Setting.data.navigation.value = JSON.stringify(value)
            }
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
        addNav(){
            this.navigations.push(this.nav)
            this.$store.state.Setting.data.navigations.value = JSON.stringify(this.navigations)
            this.nav = {}
        },
        removeNav(index){
            this.navigations.splice(index, 1)
            this.$store.state.Setting.data.navigations.value = JSON.stringify(this.navigations)
        }
    },
    beforeMount(){
        fetchSettings(this.$store)
    },
    components:{
        Draggable
    }
}
</script>
<style>
    .input-group-btn{
        border-right: 10px solid transparent;
        border-left: 10px solid transparent;
    }
    .outer{
        margin-left: -20px;
    }
</style>