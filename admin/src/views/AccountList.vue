<template>
<div class="app-content">
    <div class="app-content-body">
        <div class="bg-light lter b-b wrapper-md clearfix">
            <h1 class="m-n font-thin h3 pull-left">Accounts</h1>
            <a href="javascript:void(0)" class="btn btn-primary pull-right" @click="isAddModalShow=true">Add Account</a>
        </div>
        <modal title="Add Account" ok-text="Save" :is-show="isAddModalShow" @close="isAddModalShow=false" :on-ok="addAccount" >
            <form class="form-horizontal" @submit.prevent="save">
                <div class="form-group">
                    <label class="col-lg-2 control-label">Name</label>
                    <div class="col-lg-10">
                        <input type="text" class="form-control" v-model="account.name">
                        <span class="help-block m-b-none">Use your real name so people can recognise you</span>
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-lg-2 control-label">Email</label>
                    <div class="col-lg-10">
                        <input type="text" class="form-control" v-model="account.email">
                        <span class="help-block m-b-none">Used for notifications</span>
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-lg-2 control-label">Password</label>
                    <div class="col-lg-10">
                        <input type="password" class="form-control" v-model="account.password">
                        <span class="help-block m-b-none">Used for signin</span>
                    </div>
                </div>
            </form>
        </modal>
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
                    <span class="pull-right label bg-primary inline m-t-sm">Admin</span>
                </router-link>
            </div>
        </div>
    </div>
</div>
</template>
<script>
    import toastr from 'toastr'
    import 'toastr/build/toastr.css'
    import Modal from '../components/Modal.vue'

    function fetchAccounts(store, page){
        let params = {
            p: page?page:1
        }
        return store.dispatch('account/FETCH_ITEMS', {path: 'accounts', params:params})
    }

    export default{
        name: 'AccountList',
        data(){
            return{
                account: {},
                isAddModalShow: false
            }
        },
        computed:{
            accounts(){
                return this.$store.getters['account/GET_ITEMS']().data
            },
            page(){return this.$store.getters['account/GET_ITEMS']().page}
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
                }, (error) => {
                    console.error(error)
                })
            }
        },
        beforeMount(){
            fetchAccounts(this.$store)
        },
        components:{
            Modal
        }
    }
</script>
<style>
</style>