<template>
    <div class="modal-wrap" v-show="isActive">
        <div class="modal-backdrop fade in"></div>
        <div tabindex="-1" role="dialog" class="modal fade in" @click.self="backdropClose">
            <div class="modal-dialog" :class="{'modal-sm': size == 'sm', 'modal-lg': size == 'lg'}">
                <div class="modal-content" modal-transclude>
                    <div class="modal-header" v-if="showHeader">
                        <slot name="header"><h3 class="modal-title">{{title}}</h3></slot>
                    </div>
                    <div class="modal-body">
                        <slot></slot>
                    </div>
                    <div class="modal-footer" v-if="showFooter">
                        <slot name="footer">
                            <button class="btn btn-default" @click="handleCancel" v-if="showCancel">{{ cancelText }}</button>
                            <button class="btn btn-primary" @click="handleOk" v-if="showOk">{{ okText }}</button>
                        </slot>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    export default{
        props: {
            isShow: { type: Boolean, default: false },
            title: { type: String },
            okText: { type: String, default: 'OK' },
            cancelText: { type: String, default: 'Cancel' },
            onOk: { type: Function, default() {} },
            onCancel: { type: Function, default() {}},
            backdrop: { type: Boolean, default: true },
            backdropClosable: { type: Boolean, default: true},
            okLoading: { type: Boolean, default: false },
            width: { type: Number, default: 640 },
            showOk: { type: Boolean, default: true },
            showCancel: { type: Boolean, default: true },
            transition: { type: String, default: 'fade' },
            showHeader: { type: Boolean, default: true },
            showFooter: { type: Boolean, default: true },
            size:{type:String, default: ''}
        },
        data() {
            return {
              isActive: false,
              isLoading: false,
            };
        },
        computed: {
            modalWidth() {
              if (this.width !== 640 && this.width !== 0) {
                return { width: `${this.width}px` };
              }
              return null;
            },
        },
        methods: {
            active() {
              this.isActive = true;
            },
            handleOk() {
              if (this.okLoading) {
                this.isLoading = true;
                this.onOk();
              } else {
                this.onOk();
                this.handleClose();
              }
            },
            handleCancel() {
              this.onCancel();
              this.handleClose();
            },
            handleClose() {
              this.$emit('close');
            },
            backdropClose() {
              if (this.backdropClosable) {
                this.handleCancel();
              }
            },
        },
        watch: {
            isShow(val) {
              this.isActive = val;
              if (!val && this.isLoading) {
                this.isLoading = false;
              }
            },
        },
        mounted() {
            this.$nextTick(() => {
              document.body.appendChild(this.$el);
            });
        },
        beforeDestroy() {
            this.$el.remove();
        }
    }
</script>
<style>
    .modal{
        display: block;
    }
</style>