<template>
	<div class="result-id" :class="{ 'is-empty': !result }" v-if="fetched">
		<EmptyCard v-if="!result">
			<template v-slot:title>
				Id não encontrado
			</template>
		</EmptyCard>
		<div class="viewer-wrapper" v-else>
			<JsonEditorSchema :jsonParams="result ? result : '{}'" :readOnly="true"/>
			<v-btn class="mt-5" color="error" @click="deleteResult" :disabled="deletingResult">Excluir</v-btn>
		</div>
	</div>
	<div class="loading" v-else>
		<v-progress-circular indeterminate :size="100" :width="2"/>
	</div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
    import EmptyCard from '@/components/EmptyCard.vue';
	import JsonEditorSchema from '@/components/JsonEditorSchema.vue';
	import axios from 'axios'

	@Component({
		components: {
            EmptyCard,
			JsonEditorSchema
		}
	})
	export default class ResultId extends Vue {
		private result: any = null;
		private fetched: boolean = false;
		private deletingResult: boolean = false;

		async created() {
			const id = this.$route.params.id;
			this.result = (await axios.get(`/api/results/id/${id}`)).data;
			this.fetched = true;
		}

		async deleteResult() {
			this.deletingResult = true;
			try {
				let success = (await axios.post('/api/results/delete/', {result_id: this.result['id']})).data;
				this.$toasted.show('Resultado excluído!').goAway(2000);
				this.$router.push({name: 'results'});
			}
			catch (error) {
				this.$toasted.show('Erro ao excluir resultado!', {
					type: 'error'
				}).goAway(2000);
			}
			this.deletingResult = false;
		}
	}
</script>

<style lang="scss" scoped>
	.viewer-wrapper {
		button {
			margin-top: 10px;
		}
	}
</style>

