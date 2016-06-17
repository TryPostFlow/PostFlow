<template>
    <header class="main-header no-cover">
        <div class="container yue">
            <div class="main-header-content inner">
                <h1 class="page-title">一任阶前点滴到天明</h1>
                <p class="page-description">Thoughts, stories and ideas.</p>
            </div>
        </div>
    </header>
    <main id="content" class="content container yue" role="main">
        <article class="post" v-for="post in posts" track-by="id">
            <header class="post-header">
                <h2 class="post-title">
                    <a v-link="{ name: 'post', params: { post_id: post.slug }}">{{post.title}}</a>
                </h2>
            </header>
            <section class="post-excerpt">
                <p>{{{post.content}}} <a class="read-more"  v-link="{ name: 'post', params: { post_id: post.slug }}">»</a></p>
            </section>
            <footer class="post-meta">
                <img class="author-thumb" src="//www.gravatar.com/avatar/08522ef89ebc3b53ffdf3bac9b6e53ea?s=250&amp;d=mm&amp;r=x" alt="shawnxie" nopin="nopin">
                <a href="/author/shawnxie/">shawnxie</a>
                 on <a href="/tag/getting-started/">Getting Started</a>
                <time class="post-date" datetime="{{post.created_at}}">{{post.created_at | format "Do MMMM YYYY"}}</time>
            </footer>
        </article>

        <nav class="pagination" role="navigation">
            <span class="page-number">Page 1 of 1</span>
        </nav>
    </main>
</template>

<script>
import {API} from '../api.js'
// import Item from './post-item.vue'

export default {
    name: 'Home',
    // components: {
    //     Item
    // },
    data () {
        return {
            posts: []
        }
    },
    route: {
        data () {
            var resource = this.$resource(API.POST)
            resource.query(function(data, status, request){
                this.posts = data
            })
        }
    }
}
</script>
