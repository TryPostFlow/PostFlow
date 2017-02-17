<template>
<div class="app-content">
    <div class="app-content-body">
        <div class="bg-light lter b-b wrapper-md clearfix">
            <h1 class="m-n font-thin h3 pull-left">Accounts</h1>
            <a href="javascript:void(0)" class="btn btn-primary pull-right">Add</a>
        </div>
        <div class="wrapper-md">
            <div class="panel no-border">
                <div class="list-group list-group-lg list-group-sp">
                    <a class="list-group-item clearfix" v-for="account in accounts">
                        <span class="pull-left thumb-sm avatar m-r">
                            <img :src="account.avatar">
                        </span>
                        
                        <span class="pull-left">
                            <a href="">{{account.name}}</a>
                            <small class="text-muted clear text-ellipsis">{{account.email}}</small>
                        </span>
                        <span class="pull-right label bg-primary inline m-t-sm">Admin</span>
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
    function fetchAccounts(store, page){
        let params = {
            p: page?page:1
        }
        return store.dispatch('account/FETCH_ITEMS', {path: 'accounts', params:params})
    }

    export default{
        name: 'AccountList',
        computed:{
            accounts(){
                return this.$store.getters['account/GET_ITEMS']().data
            },
            page(){return this.$store.getters['account/GET_ITEMS']().page}
        },
        beforeMount(){
            fetchAccounts(this.$store)
        },
        // watch:{
        //     '$route': function(){
        //         if (this.$route.name == 'TagList'){
        //             fetchTags(this.$store)
        //         }
        //     }
        // }
    }
</script>
<style>
</style>