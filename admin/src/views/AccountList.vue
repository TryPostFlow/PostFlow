<template>
<div class="app-content">
    <div class="app-content-body">
        <div class="bg-light lter b-b wrapper-md clearfix">
            <h1 class="m-n font-thin h3 pull-left">Accounts</h1>
            <a href="javascript:void(0)" class="btn btn-primary pull-right" @click="isAddModalShow=true">Add Account</a>
        </div>
        <div class="hbox hbox-auto-xs hbox-auto-sm">
            <div class="col w-md bg-light dk b-r bg-auto">
                <div class="wrapper">
                    <ul class="nav nav-pills nav-stacked nav-sm roles">
                        <li>
                            <router-link :to="{name:'AccountList'}">
                                <i class="fa fa-fw fa-circle text-muted" color="#23b7e5" label-color="" style="color: rgb(35, 183, 229);"></i>
                                All
                            </router-link
                        </li>
                        <li v-for="role in roles" >
                            <router-link :to="{name:'AccountList', query:{'role':role.id}}">
                                <i class="fa fa-fw fa-circle text-muted" color="#23b7e5" label-color="" style="color: rgb(35, 183, 229);"></i>
                                {{role.name}}
                                <span class="pull-right" @click.prevent="editRole(role.id)"><i class="fa fa-pencil"></i></span>
                            </router-link>
                        </li>
                        <li>
                            <router-link class="btn btn-sm btn-danger" :to="{name:'RoleCreate'}">New Role</router-link>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="col">
                <div class="wrapper-md">
                    <div class="list-group list-group-lg list-group-sp">
                        <router-link class="list-group-item clearfix" :to="{name:'AccountEdit', params:{account_id:account.id}}" v-for="account in accounts">
                            <span class="pull-left thumb-sm avatar m-r">
                                <img :src="account.avatar">
                            </span>
                            
                            <span class="pull-left">
                                <a href="">{{account.name}}</a>
                                <small class="text-muted clear text-ellipsis">{{account.email}}</small>
                            </span>
                            <span class="pull-right label bg-primary inline m-t-sm" v-if="account.primary_role">
                                {{account.primary_role.name}}
                            </span>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <modal title="Add Account" ok-text="Save" :is-show="isAddModalShow" :ok-loading="true" @close="isAddModalShow=false" :on-ok="addAccount" >
        <form class="form-horizontal" @submit.prevent="save">
            <div class="form-group" :class="{'has-error':'name' in error}">
                <label class="col-lg-2 control-label">Name</label>
                <div class="col-lg-10">
                    <input type="text" class="form-control" v-model="account.name">
                    <span class="help-block m-b-none">
                        {{'name' in error?error['name'][0]:'Use your real name so people can recognise you'}}
                    </span>
                </div>
            </div>
            <div class="form-group" :class="{'has-error':'email' in error}">
                <label class="col-lg-2 control-label">Email</label>
                <div class="col-lg-10">
                    <input type="text" class="form-control" v-model="account.email">
                    <span class="help-block m-b-none">
                        {{'email' in error?error['email'][0]:'Used for notifications'}}
                    </span>
                </div>
            </div>
            <div class="form-group" :class="{'has-error':'password' in error}">
                <label class="col-lg-2 control-label">Password</label>
                <div class="col-lg-10">
                    <input type="password" class="form-control" v-model="account.password">
                    <span class="help-block m-b-none">
                        {{'password' in error?error['password'][0]:'Used for signin'}}
                    </span>
                </div>
            </div>
        </form>
    </modal>
</div>
</template>
<script>
    import toastr from 'toastr'
    import 'toastr/build/toastr.css'
    import Modal from '../components/Modal.vue'

    function fetchAccounts(store){
        let params = {
            page: store.state.route.query.page || 1,
            role: store.state.route.query.role
        }
        return store.dispatch('account/FETCH_ITEMS', {path: 'accounts', params:params})
    }

    function fetchRoles(store){
        let params = {
            page: 1
        }
        return store.dispatch('role/FETCH_ITEMS', {path: 'roles', params:params})
    }

    export default{
        name: 'AccountList',
        data(){
            return{
                account: {},
                isAddModalShow: false,
                error:{}
            }
        },
        computed:{
            accounts(){
                return this.$store.getters['account/GET_ITEMS']().data
            },
            page(){return this.$store.getters['account/GET_ITEMS']().page},
            roles(){return this.$store.getters['role/GET_ITEMS']().data}
        },
        methods:{
            addAccount(){
                this.$store.dispatch(
                'account/CREATE_ITEM',
                {
                    path: `accounts`,
                    params: this.account
                }).then((response)=>{
                    this.account = {}
                    fetchAccounts(this.$store)
                    toastr.options.positionClass = 'toast-bottom-right';
                    toastr.success('Add account successfully.', {timeOut: 3000})
                    this.isAddModalShow = !this.isAddModalShow
                }, (error) => {
                    this.error = error.error
                })
            },
            editRole(role_id){
                this.$router.push({name:'RoleEdit', params:{role_id: role_id}})
            }
        },
        watch:{
            '$route':function(){
                fetchAccounts(this.$store)
            }
        },
        beforeMount(){
            fetchAccounts(this.$store)
            fetchRoles(this.$store)
        },
        components:{
            Modal
        }
    }
</script>
<style>
.roles a span{
    display:none;
}
.roles a:hover span{
    display: block;
}
</style>