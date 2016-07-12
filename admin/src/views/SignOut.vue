<template>
    <!-- must have a line although it's empty -->
</template>
<script>
    export default {
        name: 'SignOut',
        created: function(){
            localStorage.removeItem('auth')
            this.$route.router.go({name: 'SignIn'})
        }
    }
</script>
<style>
    
</style>