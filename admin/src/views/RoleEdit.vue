<template>
<div class="app-content">
    <div class="app-content-body">
        <div class="bg-light lter b-b wrapper-md clearfix">
            <h1 class="m-n font-thin h3 pull-left">
                <router-link class="btn btn-primary" :to="{name:'AccountList'}">Back</router-link>
            </h1>
        </div>
        <div class="wrapper-md">
            <form class="form-horizontal" @submit.prevent="save">
                <div class="form-group" :class="{'has-error':'name' in roleError}">
                    <label class="col-lg-2 control-label">Name</label>
                    <div class="col-lg-10">
                        <input type="text" class="form-control" v-model="role.name">
                        <span class="help-block m-b-none">
                            {{'name' in roleError?roleError['name'][0]:'Use your real name so people can recognise you'}}
                        </span>
                    </div>
                </div>
                <div class="form-group" :class="{'has-error':'description' in roleError}">
                    <label class="col-lg-2 control-label">Description</label>
                    <div class="col-lg-10">
                        <textarea type="text" class="form-control" v-model="role.description">
                        </textarea>
                        <span class="help-block m-b-none">
                            {{'description' in roleError?roleError['description'][0]:'Used for notifications'}}
                        </span>
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-lg-2 control-label">Permissions</label>
                    <div class="col-lg-10">
                        <div v-for="group_permission in permissions">
                            {{group_permission.name}}
                            <div class="row">
                                <div class="checkbox col-md-4" v-for="permission in group_permission.permissions">
                                    <label class="i-checks i-checks-sm">
                                        <input type="checkbox" :value="permission" v-model="role.permissions">
                                        <i></i>
                                        {{permission.action_name}}
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="form-group">
                  <div class="col-lg-offset-2 col-lg-10">
                    <button type="submit" class="btn btn-primary text-u-c" @click.stop.prevent="save">Save</button>
                    <button type="submit" class="btn btn-link text-danger text-u-c" @click.stop.prevent="isRemoveModalShow=true"><i class="fa fa-trash"></i> Delete Role</button>
                  </div>
                </div>
            </form>
        </div>
    </div>

    <modal title="Delete Role" ok-text="Sure" :is-show="isRemoveModalShow" :ok-loading="true" @close="isRemoveModalShow=false" :on-ok="remove" >
        <p>Are you sure?</p>
    </modal>
</div>
</template>

<script>
    import toastr from 'toastr'
    import 'toastr/build/toastr.css'

    import Modal from '../components/Modal.vue'
    import axios from '../store/constants/api'

    function fetchRole(store){
        return store.dispatch(
            'role/FETCH_ITEM',
            {
                path: `roles/${store.state.route.params.role_id}`,
                params: {
                    id: store.state.route.params.role_id
                }
            })
    }

    function fetchPermissions(store){
        return store.dispatch('permission/FETCH_ITEMS', {path: 'permissions?format=group', index:'object_type'})
    }

    export default{
        name: 'RoleEdit',
        data(){
            return{
                roleError: {},
                isRemoveModalShow: false
            }
        },
        computed:{
            role(){
                return this.$store.getters['role/GET_ITEM'](this.$store.state.route.params.role_id) || {}
            },
            permissions(){
                return this.$store.getters['permission/GET_ITEMS']().data
            }
        },
        beforeMount(){
            fetchRole(this.$store)
            fetchPermissions(this.$store)
        },
        methods:{
            save(){
                this.$store.dispatch(
                'role/UPDATE_ITEM',
                {
                    path: `roles/${this.$store.state.route.params.role_id}`,
                    params: this.role
                })
                .then(()=>{
                    toastr.options.positionClass = 'toast-bottom-right';
                    toastr.success('Save successfully.', {timeOut: 3000})
                }, (error) => {
                    this.roleError = {}
                    this.roleError = error.error
                })
                
            },
            remove(){
                this.$store.dispatch(
                'role/DELETE_ITEM',
                {
                    path: `roles/${this.$store.state.route.params.role_id}`,
                    params:{
                        key: this.$store.state.route.params.role_id
                    }
                }).then(()=>{
                    toastr.options.positionClass = 'toast-bottom-right';
                    toastr.success('Delete successfully.', {timeOut: 3000})
                    this.isRemoveModalShow = false
                    this.$router.push({name:'AccountList'})

                })
            }
        },
        components:{
            Modal
        }
    }
</script>
<style>
</style>