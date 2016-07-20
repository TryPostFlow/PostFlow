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
    import marked from 'marked'
    var $ = require('jquery')

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
        // computed: {
        //     content: function(){
        //         var h = marked(this.markdown)
        //         this.updateImagePlaceholders(h)
        //         return h
        //     }
        // },
        filters: {
            'marked': marked
        },
        methods:{
            updateImagePlaceholders: function(content) {
                var imgPlaceholders = $(content).find('p').filter(function() {
                    return (/^(?:\{<(.*?)>\})?!(?:\[([^\n\]]*)\])(?:\(([^\n\]]*)\))?$/gim).test($(this).text());
                });

                $(imgPlaceholders).each(function( index ) {
                    console.log(index)
                    // var elemindex = index,
                    //     self = $(this),
                    //     altText = self.text();

                    // (function(){

                    //     self.dropzone({ 
                    //         url: "/article/imgupload",
                    //         success: function( file, response ){                            
                    //             var holderP = $(file.previewElement).closest("p"),

                    //                 // Update the image path in markdown
                    //                 imgHolderMardown = $(".CodeMirror-code").find('pre').filter(function() {
                    //                     return (/^(?:\{<(.*?)>\})?!(?:\[([^\n\]]*)\])(?:\(([^\n\]]*)\))?$/gim).test(self.text()) && (self.find("span").length === 0);
                    //                 }),

                    //                 // Get markdown
                    //                 editorOrigVal = editor.getValue(),
                    //                 nth = 0,
                    //                 newMarkdown = editorOrigVal.replace(/^(?:\{<(.*?)>\})?!(?:\[([^\n\]]*)\])(:\(([^\n\]]*)\))?$/gim, function (match, i, original){
                    //                     nth++;
                    //                     return (nth === (elemindex+1)) ? (match + "(" + response.path +")") : match;
                    //                 });
                    //                 editor.setValue( newMarkdown );

                    //             // Set image instead of placeholder
                    //             holderP.removeClass("dropzone").html('<img src="'+ response.path +'"/>');
                    //         }
                    //     }).addClass("dropzone");
                    // }());
                })
            }
        },
        ready(){
            // this.updatePreview()
            this.$watch('markdown', function (val) {
              this.content = marked(val)
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