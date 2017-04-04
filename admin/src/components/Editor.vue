<template>
    <div class="hbox hbox-auto-xs hbox-auto-sm bg-white">
        <div class="col lt b-r">
            <div class="vbox">
                <div class="row-row">
                    <div class="cell scrollable hover">
                        <div class="cell-inner">
                            <textarea id="markdown-editor" class="form-control no-radius no-border no-bg wrapper-lg text-md markdown-editor" style="height:100%;" v-model="value.markdown"></textarea>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col">
            <div class="vbox">
                <div class="row-row">
                    <div class="cell scrollable hover">
                        <div class="cell-inner">
                            <div class="wrapper yue rendered-markdown" v-html="content">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import marked from 'marked'
    import $ from 'jQuery'
    var Dropzone = require("dropzone");
    import '../css/yue.css'
    import '../css/dropzone.css'

    export default{
        name: 'Editor',
        data(){
            return {
                auth: JSON.parse(localStorage.getItem('auth'))
            }
        },
        props: {
            value: {
                type: Object,
                default:function(){
                    return {
                        markdown: '',
                        content: ''
                    }
                }
            }
        },
        computed: {
            content: function(){
                return this.value.markdown?marked(this.value.markdown):this.value.content
            }
        },
        filters: {
            'marked': marked
        },
        methods:{
            updateImagePlaceholders: function() {
                    var self= this;
                    var plist = Array.prototype.slice.call(document.querySelectorAll('.rendered-markdown p'));
                    var imgPlaceholders = plist.filter(function(element) {
                        // console.log(element)
                        if ($(element).find('img').length > 0) {
                            return $($(element).find('img')[0]).attr('src') == '';
                        };
                    });
                    // console.log('length: '+imgPlaceholders.length)
                    Dropzone.autoDiscover = false;
                    imgPlaceholders.forEach(
                        function(element, index){
                            // console.log('element'+element)
                            // console.log('index'+index)
                            var elemindex = index
                            // self = $(this),
                            // altText = self.text();

                            element.setAttribute("class", "dropzone");
                            $($(element).find('img')[0]).remove()
                            var url = '/api/images'
                            var dropzone = new Dropzone(element, {
                                url: url,
                                paramName: 'file',
                                headers:{
                                    'Authorization': 'Bearer ' + self.auth.access_token
                                },
                                success: function(file, response){
                                    var holderP = $(file.previewElement).closest("p")

                                    // Get markdown
                                    var nth = 0;
                                    var newMarkdown = self.value.markdown.replace(/(!\[.*?\]\()(\))/g, function (whole, a, b){
                                        nth++;
                                        // console.log('nth: '+nth)
                                        // console.log('elemindex: ' + elemindex)
                                        //  console.log(nth === (elemindex+1))
                                        // console.log('whole: '+ whole)
                                        // console.log('a: '+ a)
                                        // console.log('b: '+ b)
                                        return (nth === (elemindex+1)) ? (a + response.url +')') : a+b;
                                    });
                                    self.value.markdown = newMarkdown
                                    // console.log(self.markdown)

                                    // Set image instead of placeholder
                                    holderP.removeClass("dropzone").html('<img src="'+ response.url +'"/>');
                                }
                            });
                        }
                    );
                }
        },
        mounted(){
            this.updateImagePlaceholders()

            this.$watch('content', function(val){
                this.updateImagePlaceholders()
                this.value.content = this.content
                this.$emit('input', this.value)
            })

        }
    }
</script>
<style>
    .markdown-editor{
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        overflow: auto;
        -webkit-overflow-scrolling: touch;
        padding: 21px 20px 36px;
        max-width: 100%;
        height: 100%;
        border: 0;
        color: #3d4043;
        font-family: Consolas,"Liberation Mono",Menlo,Courier,monospace;
        font-size: 1.6rem;
        line-height: 2.5rem;
        resize: none;
    }
</style>