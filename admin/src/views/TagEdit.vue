<template>
<div class="col w-xxl">
    <div class="vbox">
        <div class="row-row">
            <div class="cell">
                <div class="cell-inner">
                    <div class="wrapper b-b">
                        <a v-link="{ name: 'TagCreate'}" class="btn btn-sm btn-default">New TAG</a>
                    </div>
                    <div class="wrapper b-b clear">
                        <div class="font-bold m-b">Tag Settings</div>
                        <form role="form" v-on:submit.prevent>
                            <div class="form-group">
                                <label>Name</label>
                                <input type="text" class="form-control" v-model="tag.name" @blur="save">
                            </div>
                            <div class="form-group">
                                <label>URL</label>
                                <input type="text" class="form-control" v-model="tag.slug">
                            </div>
                            <div class="form-group">
                                <label>Description</label>
                                <textarea class="form-control" name="description" id="description" cols="30" rows="10" v-model="tag.description"></textarea>
                            </div>
                            <div class="form-group">
                                <button type="submit" class="btn btn-sm btn-success pull-left" @click="save"><i class="fa fa-save"></i> SAVE TAG</button>
                                <button type="submit" class="btn btn-sm btn-link text-danger pull-right"><i class="fa fa-trash"></i> DELETE TAG</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

    </div>
</div>
</template>
<script>
import {API} from '../api.js'

export default{
    name: 'TagEdit',
    data () {
        return {
            tag: {},
            tags: []
        }
    },
    route: {
        data ({ to }) {
            var resource = this.$resource(API.TAG)
            resource.get({id: to.params.tag_id}).then((response) => {
                this.tag = response.data
            })
        }
    },
    methods: {
        save: function(){
            let resource = this.$resource(API.TAG)
            resource.update({id: this.tag.id},this.tag).then(
                (response) => {
                this.tag = response.data
            })
        }
    }
}
</script>
<style>

</style>