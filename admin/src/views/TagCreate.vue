<template>
<div class="col w-xxl">
    <div class="vbox">
        <div class="row-row">
            <div class="cell">
                <div class="cell-inner">
                    <div class="wrapper b-b clear">
                        <div class="font-bold m-b">Tag Settings</div>
                        <form role="form" v-on:submit.prevent>
                            <div class="form-group">
                                <label>Name</label>
                                <input type="text" class="form-control" v-model="tag.name">
                            </div>
                            <div class="form-group">
                                <label>URL</label>
                                <input type="text" class="form-control" v-model="tag.slug">
                            </div>
                            <div class="form-group">
                                <label>Description</label>
                                <textarea class="form-control" name="description" id="description" cols="30" rows="10" v-model="tag.description"></textarea>
                            </div>
                            <button type="submit" class="btn btn-sm btn-success" @click="save"><i class="fa fa-save"></i> SAVE TAG</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>

    </div>
</div>
</template>
<script>
import toastr from 'toastr'
import 'toastr/build/toastr.css'

export default{
    name: 'TagCreate',
    data () {
        return {
            tag: {}
        }
    },
    methods: {
        save: function(){
            this.$store.dispatch(
                'tag/CREATE_ITEM',
                {
                    path: `tags`,
                    params: this.tag
                }
            )
            .then((response)=>{
                toastr.options.positionClass = 'toast-bottom-right';
                toastr.success('Save successfully.', {timeOut: 3000})
                this.$router.push({name:'TagEdit', params:{tag_id: response.data.id}})
            })
        }
    }
}
</script>
<style>

</style>