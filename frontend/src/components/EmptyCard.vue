<template>
    <div class="empty">
        <div class="empty-icon">
            <i class="icon icon-more-horiz"></i>
        </div>
        <p class="empty-title h5">
            <slot name="title">
                Nenhum resultado foi encontrado
            </slot>
        </p>
        <p class="empty-subtitle">
            <slot name="description">
                Tente <router-link :to="{name:'strat-create'}">criar</router-link> uma nova estratégia ou <router-link :to="{name:'strat-run'}">executar</router-link> uma já existente.
            </slot>
        </p>
    </div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	
	@Component({})
	export default class EmptyCard extends Vue { }
</script>

<style lang="scss" scoped>

</style>
