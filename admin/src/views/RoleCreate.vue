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
                            {{group_permission.group}}
                            <div class="row">
                                <div class="checkbox col-md-4" v-for="permission in group_permission.permissions">
                                    <label class="i-checks i-checks-sm">
                                        <input type="checkbox" :value="permission" v-model="role.permissions">
                                        <i></i>
                                        {{permission.object_type}} {{permission.action_type}}
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="form-group">
                  <div class="col-lg-offset-2 col-lg-10">
                    <button type="submit" class="btn btn-primary text-u-c" @click.stop.prevent="save">Save</button>
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

    import Modal from '../components/Modal.vue'
    import axios from '../store/constants/api'

    function fetchPermissions(store){
        return store.dispatch('permission/FETCH_ITEMS', {path: 'permissions?format=group', index:'group'})
    }

    export default{
        name: 'RoleCreate',
        data(){
            return{
                role:{permissions:[]},
                roleError: {}
            }
        },
        computed:{
            permissions(){
                return this.$store.getters['permission/GET_ITEMS']().data
            }
        },
        beforeMount(){
            fetchPermissions(this.$store)
        },
        methods:{
            save(){
                this.$store.dispatch(
                'role/CREATE_ITEM',
                {
                    path: `roles`,
                    params: this.role
                })
                .then((response)=>{
                    toastr.options.positionClass = 'toast-bottom-right';
                    toastr.success('Save successfully.', {timeOut: 3000})
                    this.$router.push({name:'RoleEdit', params:{role_id:response.data.id}})
                }, (error) => {
                    this.roleError = {}
                    this.roleError = error.error
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