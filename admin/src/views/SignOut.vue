<template>
    <!-- must have a line although it's empty -->
</template>
<script>
    export default {
        name: 'SignOut',
        created: function(){
            localStorage.removeItem('auth')
            this.$route.router.go({name: 'SignIn'})
            this.$root.isLogin = false
        }
    }
</script>
<style>
    
</style>