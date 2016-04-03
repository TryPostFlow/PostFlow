<template>
<div class="app" v-bind:class="{'app-header-fixed':settings.headerFixed, 'app-aside-fixed':settings.asideFixed, 'app-aside-folded':settings.asideFolded, 'app-aside-dock':settings.asideDock, 'container':settings.container}">
    <slot></slot>
</div>
</template>
<script>
export default{
    props: ['settings']
}
</script>
<style>
@import "bootstrap";
@import "font-awesome";
@import "variables.css";
@import "mixins.css";
@import "reset.css";
@import "layout.css";
@import "layout.boxed.css";
@import "nav.css";
@import "nav.offscreen.css";
@import "nav.dock.css";
@import "arrow.css";
@import "buttons.css";
@import "colors.css";
@import "utilities.css";
</style>