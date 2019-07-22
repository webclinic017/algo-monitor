<template>
    <div id="main-sidebar" class="sidebar">
        <div class="brand">
            <h5>
                Algo Monitor
            </h5>
        </div>
        <ul class="nav">
            <li class="nav-item">
                <router-link :to="{name:'home'}" exact>Home</router-link>
            </li>
            <li class="nav-item">
                <router-link :to="{name:'results'}" exact>Resultados</router-link>
            </li>
            <li class="nav-item">
                <a href="#">Estratégias</a>
                <ul class="nav">
                    <li class="nav-item">
                        <router-link :to="{name:'strat-run'}" exact>Rodar</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link :to="{name:'strat-create'}" exact>Criar</router-link>
                    </li>
                </ul>
            </li>
        </ul>
    </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';
    
    @Component({})
	export default class Sidebar extends Vue {

    }
</script>

<style lang="scss" scoped>
    .brand {
        padding: 5px .4rem 10px;
        h5 {
            margin: 0;
        }
    }

    .router-link-active {
        color: #505c6e;
        font-weight: 700;
    }
</style>


