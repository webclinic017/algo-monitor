<template>
  <div class="result-id">
		<div>
			<JsonEditor :jsonParams="result ? result : '{}'" :readOnly="true"/>
		</div>
  </div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import axios from 'axios'
	import JsonEditor from '@/components/JsonEditor.vue';

	@Component({
		components: {
			JsonEditor
		}
	})
	export default class ResultId extends Vue {
		private result: any = null;

		async created() {
			const id = this.$route.params.id;
			this.result = (await axios.get(`/api/results/id/${id}`)).data;
		}
	}
</script>
