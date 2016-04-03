<template></template>
<script>
    export default {
        created: function(){
            localStorage.removeItem('auth')
            this.$route.router.go({name: 'SignIn'})
            this.$root.isLogin = false
        }
    }
</script>
<style></style>