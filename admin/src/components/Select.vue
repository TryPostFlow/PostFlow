<template>
    <select multiple="{{multiple}}" style="width: 100%"></select>
</template>
<script>
var $ = require('jquery')
var select2 = require('select2')

export default{
    props: {
        multiple: {
            type: String,
            default: false
        },
        selected: {
            twoWay: true
        },
        tags: {
            type: Boolean,
            default: false
        }
    },
            route: {
            data ({ to }) {
              console.log('select route')
            }
      },
    compiled(){
      console.log('compile')
    },
    ready(){
      console.log('select ready')
        var self = this
        var select = $(this.$el)

        function formatRepo (repo) {
          return repo.name
        }

        function formatRepoSelection (repo) {
          return repo.name
        }

        select.select2({
          tags: this.tags,
          ajax: {
            url: 'http://127.0.0.1:5000/tags',
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
          $.each(select.select2('data'), function (key, value) {
            data.push({
              id: parseInt(value.id)? parseInt(value.id): null,
              name: value.text || value.name,
            text: value.text || value.name})
          })
          self.selected = data
        })
    },
    watch: {
        'selected': function(val, oldVal){
            var select = $(this.$el)
            select.html('')
            $.each(val, function (key, value) {
              var $option = $('<option selected>Loading...</option>')
              $option.text(value.name).val(value.id)
              $option.removeData()
              select.append($option)
            })
            select.select2({
              tags: []
            })
        }
    },

    beforeDestroy(){
      console.log('select before destroy')
        $(this.$el).off().select2('destroy')
    },
    destroyed(){
      console.log('select destroy')
    }
}
</script>
<style>
/*@import "select2/dist/css/select2.css";*/
</style>