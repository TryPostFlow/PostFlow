<template>
    <select :multiple="multiple" style="width: 100%"></select>
</template>
<script>
import "select2/dist/css/select2.css"
var $ = require('jquery')
var select2 = require('select2')

export default{
    name: 'Select',
    props: {
        multiple: {
            type: String,
            default: false
        },
        value: {
            type: Array,
            default: function(){
              return []
            }
        },
        tags: {
            type: Boolean,
            default: false
        }
    },
    data(){
      return{
        select:$(this.$el)
      }
    },
    mounted(){
        var self = this
        self.select = $(this.$el)

        function formatRepo (repo) {
          return repo.name
        }

        function formatRepoSelection (repo) {
          return repo.name
        }

        self.select.select2({
          tags: this.tags,
          ajax: {
            url: 'http://127.0.0.1:5000/api/tags',
            dataType: 'json',
            delay: 250,
            data: function (params) {
              return {
                q: params.term,
                page: params.page
              }
            },
            processResults: function (data, params) {
              params.page = params.page || 1
              return {
                results: data
              }
            },
            cache: true
          },
          escapeMarkup: function (markup) {
            return markup; },
          minimumInputLength: 1,
          templateResult: formatRepo,
          templateSelection: formatRepoSelection
        }).on('change', function () {
          var data = []
          $.each(self.select.select2('data'), function (key, value) {
            data.push({
              id: parseInt(value.id)? parseInt(value.id): null,
              name: value.text || value.name,
            text: value.text || value.name})
          })
          // self.selected = data
          self.$emit('input', data)
        })
    },
    watch: {
      value(val){
        // select.html('')
        var self = this
        $.each(val, function (key, value) {
          var $option = $('<option selected>Loading...</option>')
          $option.text(value.name).val(value.id)
          $option.removeData()
          self.append($option)
          // select.trigger('change')
        })
        self.trigger('change.select2')
      }
    },
    destroyed(){
      $(this.$el).off().select2('destroy')
    }
}
</script>
<style>
/*@import "select2/dist/css/select2.css";*/
</style>