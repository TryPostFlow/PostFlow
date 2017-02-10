<template>
    <div class="btn-group dropdown">
      <button class="btn btn-primary" :data-target="defaultItem.dataTarget || items[0].dataTarget">{{defaultItem.text || items[0].text}}</button>
      <button class="btn btn-primary" data-toggle="dropdown"><span class="caret"></span></button>
      <ul class="dropdown-menu">
        <li v-for="item in items"><a href="#" :data-target="item.dataTarget">{{item.text}}</a></li>
      </ul>
    </div>
</template>
<script>
    import jQuery from 'jquery'
    window.jQuery = jQuery
    require('bootstrap/js/dropdown.js')

    export default{
        name: 'DropdownButton',
        props: {
            items: {
                type: Array,
                default: function(){
                    return [{dataTarget: '', text: ''}]
                }
            },
            defaultItem: {
                type: Object,
                default: function(){
                    return {dataTarget: '', text: ''}
                }
            }
        },
        methods: {
            action: function(data_target){
                this.$emit('action', data_target)
            }
        },
        mounted(){
            var self = this
            jQuery('.dropdown .btn:first-child').click(function(){self.action(jQuery(this).attr('data-target'))})
            jQuery('.dropdown-menu').on('click', 'li a', function(event){
                event.preventDefault();
                var data_target = jQuery(this).attr('data-target')
                var displayed_btn = jQuery(this).closest('.dropdown').find('.btn:first-child')
                displayed_btn.text(jQuery(this).text())
                displayed_btn.unbind('click')
                displayed_btn.bind('click', function(){console.log(data_target);self.action(data_target)})
            })
        }
    }
</script>
<style>

</style>