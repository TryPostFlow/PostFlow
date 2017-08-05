<template>
    <div class="app-content">
        <div class="app-content-body">
            <div class="wrapper-sm b-b clearfix">
                <div class="pull-left">
                    <input class="form-control input-lg no-radius no-border no-bg text-lg" type="text" v-model="post.title" placeholder="Post title">
                </div>
                <div class="pull-right">
                    <ui-dropdown-button :items='buttons' @action="save"></ui-dropdown-button>
                    <a class="btn btn-default" href="javascript:void(0)" @click="isShow=true">
                        <i class="fa fa-gear"></i>
                    </a>
                </div>
            </div>
            <div class="app-content-full h-full" style="top: 117px; bottom:50px;">
                <ui-editor v-model="post"></ui-editor>
                <ui-aside class="aside-right" title="Post Settings" :is-show="isShow" @close="isShow=false">
                    <form>
                        <div class="form-group">
                            <dropzone :image_url="post.image.url" @success="successhandler" @remove="removehandler"></dropzone>
                        </div>
                        <div class="form-group">
                            <label>Post URL</label>
                            <div class="input-group">
                                <span class="input-group-addon">
                                    <i class="fa fa-link"></i>
                                </span>
                                <input type="text" class="form-control" v-model="post.slug">
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Sync Telegram Channel</label> <input type="checkbox" v-model="post.telegram">
                        </div>
                    </form>
                </ui-aside>
            </div>
        </div>
        <div class="app-footer wrapper b-t bg-light">
            <div class="form-horizontal">
                <div class="form-group" style="margin-bottom: 0;">
                    <label for="tags" class="control-label col-lg-1">Tags</label>
                    <div class="col-lg-10">
                        <v-select v-model="tags" multiple :taggable="true" max-height='200px' :on-search="getOptions" :options="options">
                        </v-select>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import toastr from 'toastr'
import editor from '../components/Editor.vue'
import vSelect from '../components/vue-select'
import Aside from '../components/Aside.vue'
import DropdownButton from '../components/DropdownButton.vue'
import Dropzone from '../components/Dropzone.vue'

export default {
    name: 'PostsCreate',
    data() {
        return {
            post: {
                markdown: '',
                content: '',
                tags: [],
                image: {}
            },
            buttons: [
                {
                    dataTarget: 'draft',
                    text: 'Save Draft'
                },
                {
                    dataTarget: 'published',
                    text: 'Publish Now'
                }
            ],
            isShow: false,
            isDeleteShow: false,
            options: [],
            tags: []
        }
    },
    methods: {
        save: function (status) {
            this.post.status = status
            this.$store.dispatch(
                'post/CREATE_ITEM',
                {
                    path: `posts`,
                    params: this.post
                }).then((response) => {
                    toastr.options.positionClass = 'toast-bottom-right';
                    toastr.success('Save successfully.', { timeOut: 3000 })
                    this.$router.push({ name: 'PostEdit', params: { post_id: response.data.id } })
                }, (error) => {
                    console.error(error)
                })
        },
        getOptions(search, loading) {
            loading(true)
            this.$store.dispatch(
                'tag/FETCH_ITEMS',
                {
                    path: `tags`,
                    params: {
                        q: search,
                        limit: 10
                    },
                    request: 'search'
                }).then(() => {
                    this.options = []
                    this.$store.getters['tag/GET_ITEMS']('search').data.forEach(
                        item => {
                            this.options.push({ label: item.name, value: item.id })
                        }
                    )
                    loading(false)
                })
        },
        successhandler(file, response) {
            this.$set(this.post, 'image', { url: response.url, filename: response.filename })
        },
        removehandler(path) {
            this.post.image = {}
        }
    },
    watch: {
        'tags': function () {
            let tags = []
            this.tags.forEach(item => {
                if (typeof (item) == 'object') {
                    tags.push({ name: item.label, id: item.value })
                }
                else {
                    tags.push({ name: item })
                }
            })
            this.post.tags = tags
        }
    },
    components: {
        vSelect,
        'ui-editor': editor,
        'ui-dropdown-button': DropdownButton,
        'ui-aside': Aside,
        Dropzone
    }
}
</script>
<style>

</style>