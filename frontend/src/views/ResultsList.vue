<template>
  <div class="result-list">
	<ul>
		<li v-for="result in results" :key="result.id">
            <router-link :to="{name:'result-id',params:{'id':result.id}}">{{ result.id }}</router-link> |
			<router-link :to="{name:'result-label',params:{'label':result.label}}">{{ result.label }}</router-link>
		</li>
	</ul>
  </div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import axios from 'axios'

	@Component({})
	export default class ResultsList extends Vue {
		results: any[] = [];

		async created() {
			this.results = (await axios.get('/api/results')).data;
		}
	}
</script>
