<!-- Form -->

<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <input type="file" id="file" name="file">
	<input type="text" id="entry_path" name="entry_path">
	<input @click="onClick" type="button" value="Enviar">
  </div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src
	import axios from 'axios'

	@Component({
		components: {
		// HelloWorld,
		},
	})
	export default class Home extends Vue {
		created() {
			axios.get('/api/results').then(r => console.log(r));
		}

		onClick() {
			let formData = new FormData();
			let file = (<HTMLInputElement>document.querySelector('#file'));
			let entry_path = (<HTMLInputElement>document.querySelector('#entry_path'));

			formData.append('file', file.files[0]);
			formData.append('entry_path', entry_path.value)
			axios.post('/api/upload', formData, {
				headers: {
					'Content-Type': 'multipart/form-data'
				}
			})
		}
	}
</script>
