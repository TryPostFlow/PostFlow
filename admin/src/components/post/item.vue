<template>
    <div class="item">
        <p>
            <a :href="href" class="title">{{item.title}}</a>
        </p>
    </div>
</template>

<script>
    export default {
        name: 'Item',
        props: {
            item: Object
        }
    }
</script>