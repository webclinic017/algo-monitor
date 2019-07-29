<template>
	<div class="strat-list" :class="{ 'is-empty': strats.length == 0 }" v-if="strats">
		<EmptyCard v-if="strats.length == 0">
			<template v-slot:title>
				Nenhuma estratégia foi encontrada
			</template>
			<template v-slot:description>
				Tente <router-link :to="{name:'strat-create'}">criar</router-link> uma nova estratégia.
			</template>
		</EmptyCard>
		<div class="list-wrapper" v-else>
			<ul>
                <li v-for="(strat, index) in strats" v-bind:key="index">
                    <div class="li-wrapper">
                        <div class="li-text">
                            Strat Name: {{ strat.name }} | Strat ID: {{ strat.id }}
                        </div>
                        <button class="btn btn-link btn-sm" @click="removeStrat(strat.id)" v-bind:class="{disabled: deletingStrat}"><i class="icon icon-cross"></i></button>
                    </div>
                </li>
            </ul>
		</div>
	</div>
	<div class="loading loading-xlg" v-else></div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
    import EmptyCard from '@/components/EmptyCard.vue';
	import axios from 'axios';

	@Component({
		components: {
            EmptyCard
		}
	})
	export default class StratList extends Vue {
		private strats: any[] | null = null
		private deletingStrat: boolean = false;

		async created() {
			this.strats = (await axios.get('/api/strat/list')).data;
        }
        
        async removeStrat(strat_id) {
			this.deletingStrat = true;
			try {
				let success = (await axios.post('/api/strat/delete/', {strat_id: strat_id})).data;
				this.$toasted.show('Estratégia excluída!').goAway(2000);
				this.strats = this.strats!.filter(e => e.id != strat_id);
			}
			catch (error) {
				this.$toasted.show('Erro ao excluir estratégia!', {
					type: 'error'
				}).goAway(2000);
			}
			this.deletingStrat = false;
        }
	}
</script>

<style lang="scss" scoped>
    .list-wrapper {
        ul {
            margin-left: 0;
            margin-right: 0;
            list-style: none;
            li {
                margin-top: 15px;
                .li-wrapper {
                    display: inline-block;
                    padding: 5px 5px 5px 10px;
                    box-shadow: 0 0 10px 0px rgba(48, 55, 66, 0.1);
                    .li-text,
                    button {
                        display: inline-block;
                        vertical-align: middle;
                    }
                    button {
                        padding: 0 2px;
                        margin: 2px 5px;
                        line-height: 1rem;
                        height: 1.2rem;
                    }
                }
            }
        }
    }
</style>
