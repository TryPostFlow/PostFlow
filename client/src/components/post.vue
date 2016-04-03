<template>
    <header class="main-header no-cover">
        <div class="container yue">
            <div class="main-header-content inner">
                <h1 class="page-title">{{post.title}}</h1>
                <p class="page-description">
                    <a href="/author/shawnxie/">shawnxie</a> on <a href="/tag/getting-started/">Getting Started</a> <time class="post-date" datetime="{{post.created_at}}">{{post.created_at | format "Do MMMM YYYY"}}</time>
                </p>
            </div>
        </div>
    </header>
    <main id="content" class="content container" role="main">
        <article class="post">
            <section class="post-content yue">
                {{{post.content}}}
            </section>
            <footer class="post-footer">
                <figure class="author-image">
                <a class="img" href="/author/shawnxie/" style="background-image: url(//www.gravatar.com/avatar/08522ef89ebc3b53ffdf3bac9b6e53ea?s=250&amp;d=mm&amp;r=x)"><span class="hidden">shawnxie's Picture</span></a>
            </figure>
            </footer>
        </article>
    </main>
</template>

<script>
    import {API} from '../api.js'

    export default{
        name: 'Post',
        data () {
            return {
                post: {}
            }
        },
        route: {
            data ({ to }) {
                var resource = this.$resource(API.POST)
                resource.get({id: to.params.post_id}, function(data, status, request){
                    this.post = data
                })
            }
        }
    }
</script>