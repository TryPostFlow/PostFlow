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
                            <div class="wrapper yue" v-html="markdown | marked">
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

    export default{
        props: {
            markdown: {
                twoWay: true,
                type: String,
                default: ''
            }
        },
        filters: {
            'marked': marked
        },
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