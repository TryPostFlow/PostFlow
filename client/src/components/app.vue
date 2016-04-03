<template>
    <div class="site-nav">
        <div class="container yue">    
            <a v-link="{ name: 'Index'}" id="site-brand">
                <strong>Planet</strong>
            </a>
            <nav id="nav">
                <a v-link="{ name: 'Index'}">Home</a>
            </nav>
        </div>
    </div>
    
    <div class="site-wrapper">        
        <router-view keep-alive transition-mode="out-in">
        </router-view>

        <footer class="site-footer">
            <div class="container">
                <section class="copyright"><a href="http://shawnxie.ghost.io">一任阶前点滴到天明</a> © 2016</section>
                <section class="poweredby">Proudly published with <a href="https://planet.org">Planet</a></section>
            </div>
        </footer>
    </div>
</template>

<style>
    
</style>