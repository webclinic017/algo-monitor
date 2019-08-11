<template>
	<div class="not-found is-empty">
        <EmptyCard>
            <template v-slot:title>
                Erro 404
            </template>
            <template v-slot:description>
                Página não encontrada
            </template>
        </EmptyCard>
    </div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
    import EmptyCard from '../components/EmptyCard.vue';

	@Component({
        components: {
            EmptyCard
        }
    })
	export default class NotFound extends Vue { }
</script>

<style lang="scss" scoped>
    
</style>
