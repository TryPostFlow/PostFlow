<template>
    <div class="app-content">
      <div class="app-content-body">

        <div class="hbox hbox-auto-xs hbox-auto-sm">
            <div class="col w-xl bg-light dk b-r bg-auto">
                <ul class="list-group list-group-lg no-radius m-b-none m-t-n-xxs">
                </ul>
            </div>
            <div class="col">
                
            </div>
        </div>

    </div>
</div>

</template>

<script>
import {API} from '../../api.js'

export default {
    name: 'PostsList',
    data () {
        return {
            posts: []
        }
    },
    route: {
        data () {
            var resource = this.$resource(API.POST)
            resource.query().then(function(response){
                 if (response.data.length > 0) {
                    this.$route.router.go(
                        {
                            name: 'PostView',
                            params: { post_id: response.data[0].id }
                        }
                    )
                }
            })
        }
    },
    created: function(){
        var resource = this.$resource(API.POST)
        resource.query().then(function(response){
             if (response.data.length > 0) {
                this.$route.router.replace(
                    {
                        name: 'PostView',
                        params: { post_id: response.data[0].id }
                    }
                )
            }
        })
    },
    // compiled: function(){
    //     var resource = this.$resource(API.POST)
    //     resource.query().then(function(response){
    //          if (response.data.length > 0) {
    //             this.$route.router.replace(
    //                 {
    //                     name: 'PostView',
    //                     params: { post_id: response.data[0].id }
    //                 }
    //             )
    //         }
    //     })
    // }
}
</script>
