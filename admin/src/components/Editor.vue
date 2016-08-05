<template>
    <div class="hbox hbox-auto-xs hbox-auto-sm bg-white">
        <div class="col lt b-r">
            <div class="vbox">
                <div class="row-row">
                    <div class="cell scrollable hover">
                        <div class="cell-inner">
                            <textarea id="markdown-editor" class="form-control no-radius no-border no-bg wrapper-lg text-md markdown-editor" style="height:100%;" v-model="markdown"></textarea>
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
                            <!-- <div class="wrapper yue rendered-markdown"> -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import {API} from '../api.js'
    import marked from 'marked'
    import $ from 'jQuery'
    var Dropzone = require("dropzone");

    export default{
        props: {
            markdown: {
                twoWay: true,
                type: String,
                default: ''
            },
            content: {
                twoWay: true,
                type: String,
                default: ''
            }
        },
        computed: {
            content: function(){
                return marked(this.markdown)
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
                            var dropzone = new Dropzone(element, {
                                url: self.$http.options.root+'/'+API.IMAGE_UPLOAD,
                                paramName: 'image',
                                success: function(file, response){
                                    var holderP = $(file.previewElement).closest("p")

                                    // Get markdown
                                    var nth = 0;
                                    var newMarkdown = self.markdown.replace(/(!\[.*?\]\()(\))/g, function (whole, a, b){
                                        nth++;
                                        // console.log('nth: '+nth)
                                        // console.log('elemindex: ' + elemindex)
                                        //  console.log(nth === (elemindex+1))
                                        // console.log('whole: '+ whole)
                                        // console.log('a: '+ a)
                                        // console.log('b: '+ b)
                                        return (nth === (elemindex+1)) ? (a + response.path +')') : a+b;
                                    });
                                    self.markdown = newMarkdown
                                    // console.log(self.markdown)

                                    // Set image instead of placeholder
                                    holderP.removeClass("dropzone").html('<img src="'+ response.path +'"/>');
                                }
                            });
                        }
                    );
                }
        },
        ready(){
            this.updateImagePlaceholders()

            this.$watch('content', function(val){
                this.updateImagePlaceholders()
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