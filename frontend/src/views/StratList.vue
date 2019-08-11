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
            <v-list class="strats">
                <v-list-item class="list-item" two-line v-for="(strat, index) in strats" v-bind:key="index">
                    <v-list-item-content class="list-content">
                        <v-list-item-title>
                            <span>{{ strat.name }}</span>
                            <v-btn class="ml-2" text small icon @click="removeStrat(strat.id)" :disabled="deletingStrat">
                                <v-icon>mdi-close</v-icon>
                            </v-btn>
                        </v-list-item-title>
                        <v-list-item-subtitle>{{ strat.id }}</v-list-item-subtitle>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
		</div>
	</div>
	<div class="loading" v-else>
		<v-progress-circular indeterminate :size="100" :width="2"/>
	</div>
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
    .strats {
        background: transparent;
        padding: 0 0 15px;
        .list-item {
            width: 50%;
            display: inline-flex;
            padding: 0;
        }
    }
</style>
