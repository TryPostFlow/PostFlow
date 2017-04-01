<template>
<div class="app-content">
    <div class="app-content-body">
        <div class="bg-light lter b-b wrapper-md clearfix">
            <h1 class="m-n font-thin h3 pull-left">Account</h1>
        </div>
        <div class="wrapper-md">
            <form class="form-horizontal" @submit.prevent="save">
                <div class="form-group" :class="{'has-error':'name' in accountError}">
                    <label class="col-lg-2 control-label">Name</label>
                    <div class="col-lg-10">
                        <input type="text" class="form-control" v-model="account.name">
                        <span class="help-block m-b-none">
                            {{'name' in accountError?accountError['name'][0]:'Use your real name so people can recognise you'}}
                        </span>
                    </div>
                </div>
                <div class="form-group" :class="{'has-error':'email' in accountError}">
                    <label class="col-lg-2 control-label">Email</label>
                    <div class="col-lg-10">
                        <input type="text" class="form-control" v-model="account.email">
                        <span class="help-block m-b-none">
                            {{'email' in accountError?accountError['email'][0]:'Used for notifications'}}
                        </span>
                    </div>
                </div>
                <div class="form-group">
                  <div class="col-lg-offset-2 col-lg-10">
                    <button type="submit" class="btn btn-primary text-u-c" @click.stop.prevent="save">Save</button>
                    <button type="submit" class="btn btn-link text-danger text-u-c" @click.stop.prevent="isRemoveModalShow=true"><i class="fa fa-trash"></i> Delete Account</button>
                  </div>
                </div>
            </form>
            <modal title="Delete Account" ok-text="Sure" :is-show="isRemoveModalShow" :ok-loading="true" @close="isRemoveModalShow=false" :on-ok="remove" >
                <p>Are you sure?</p>
            </modal>
            <div class="line line-dashed b-b line-lg pull-in"></div>
            <form class="form-horizontal" @submit.prevent="change_password">
                <div class="form-group" :class="{'has-error':'old_password' in passwordError}">
                    <label class="col-lg-2 control-label">Old Password</label>
                    <div class="col-lg-10">
                        <input type="password" class="form-control" v-model="password.old_password">
                        <span class="help-block m-b-none" v-if="'old_password' in passwordError">{{passwordError.old_password[0]}}</span>
                    </div>
                </div>
                <div class="form-group" :class="{'has-error':'new_password' in passwordError}">
                    <label class="col-lg-2 control-label">New Password</label>
                    <div class="col-lg-10">
                        <input type="password" class="form-control" v-model="password.new_password">
                        <span class="help-block m-b-none" v-if="'new_password' in passwordError">{{passwordError.new_password[0]}}</span>
                    </div>
                </div>
                <div class="form-group" :class="{'has-error':'verify_password' in passwordError}">
                    <label class="col-lg-2 control-label">Verify Password</label>
                    <div class="col-lg-10">
                        <input type="password" class="form-control" v-model="password.verify_password">
                        <span class="help-block m-b-none" v-if="'verify_password' in passwordError">{{passwordError.verify_password[0]}}</span>
                    </div>
                </div>
                <div class="form-group">
                  <div class="col-lg-offset-2 col-lg-10">
                    <button type="submit" class="btn btn-danger text-u-c" @click.stop.prevent="change_password">Change Password</button>
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

    function fetchAccount(store){
        return store.dispatch(
            'account/FETCH_ITEM',
            {
                path: `accounts/${store.state.route.params.account_id}`,
                params: {
                    id: store.state.route.params.account_id
                }
            })
    }

    export default{
        name: 'AccountEdit',
        data(){
            return{
                password:{
                    id: null,
                    old_password: null,
                    new_password: null,
                    verify_password: null
                },
                accountError: {},
                passwordError: {},
                isRemoveModalShow: false
            }
        },
        computed:{
            account(){
                return this.$store.getters['account/GET_ITEM'](this.$store.state.route.params.account_id) || {}
            }
        },
        beforeMount(){
            fetchAccount(this.$store).then(()=>{
                this.password.id = this.account.id
            })
        },
        methods:{
            save(){
                this.$store.dispatch(
                'account/UPDATE_ITEM',
                {
                    path: `accounts/${this.$store.state.route.params.account_id}`,
                    params: this.account
                })
                .then(()=>{
                    toastr.options.positionClass = 'toast-bottom-right';
                    toastr.success('Save successfully.', {timeOut: 3000})
                }, (error) => {
                    this.accountError = {}
                    this.accountError = error.error
                })
                
            },
            change_password(){
              var vm = this
              axios.put(
                `accounts/${this.$store.state.route.params.account_id}/password`,
                this.password)
              .then(function (response) {
                vm.password = {id: vm.account.id}
                toastr.options.positionClass = 'toast-bottom-right';
                toastr.success('Change Password successfully.', {timeOut: 3000})
              })
              .catch(function(error){
                vm.passwordError = {}
                vm.passwordError = error.response.data.error
              })
            },
            remove(){
                this.$store.dispatch(
                'account/DELETE_ITEM',
                {
                    path: `accounts/${this.$store.state.route.params.account_id}`,
                    params:{
                        key: this.$store.state.route.params.account_id
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