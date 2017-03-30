<template>
    <!-- must have a line although it's empty -->
</template>
<script>
    export default {
        name: 'SignOut',
        created: function(){
            this.$store.commit('auth/DELETE_ITEM')
            this.$router.push({name: 'SignIn'})
        }
    }
</script>
<style>
    
</style>