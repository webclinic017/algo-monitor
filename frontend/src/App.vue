<template>
	<v-app class="v-app">
		<VSidebar v-model="drawer"/>
		<VHeader v-model="drawer"/>

		<!-- Sizes your content based upon application components -->
		<v-content class="v-content">

			<!-- Provides the application the proper gutter -->
			<v-container class="v-container" fluid>

				<!-- If using vue-router -->
				<router-view></router-view>
			</v-container>
		</v-content>

		<!-- <v-footer app> -->
			<!-- -->
		<!-- </v-footer> -->
	</v-app>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import VSidebar from '@/components/layout/VSidebar.vue';
	import VHeader from '@/components/layout/VHeader.vue';
	import Toasted from 'vue-toasted';
	
	Vue.use(Toasted);
	@Component({
		components: {
			VSidebar,
			VHeader
		},
	})
	export default class App extends Vue {
		private drawer: boolean | null = null;
	}
</script>

<style lang="scss">
	@import url('https://fonts.googleapis.com/css?family=Roboto&display=swap');

	body {
		font-family: 'Roboto', sans-serif;
	}

	.v-app {
		.v-content__wrap {
			display: flex;
			flex-direction: column;
			.container {
				display: flex;
				flex-direction: column;
				flex: 1;
				&>div.is-empty:only-of-type,
				&>div.loading:only-of-type {
					flex: 1;
					display: flex;
					flex-direction: column;
					justify-content: space-around;
					margin-bottom: 5%;
				}
			}
		}
	}

	.v-container {
		padding: 40px 40px !important;
	}

	.subtitle {
		color: #707070;
	}

	.empty {
		background: transparent !important;
	}

	.json-editor {
		.jsoneditor {
			min-height: 150px;
			border: thin solid #303030;
			.jsoneditor-menu {
				background-color: #303030;
				border-bottom: 1px solid #303030;
			}
		}
	}

	.jsoneditor-contextmenu ul li button {
		color: #f5f5f5 !important;
		&:hover {
			color: #1a1a1a !important;
		}
	}

	.loading {
		align-items: center;
	}

	.empty {
		// background: #f7f8f9;
		border-radius: .1rem;
		color: #66758c;
		padding: 3.2rem 1.6rem; 
		text-align: center;
	}

	.empty .empty-icon {
		// margin-bottom: .8rem;
	}

	.empty .empty-title,
	.empty .empty-subtitle {
		margin: .4rem auto;
	}

	.empty .empty-action {
		margin-top: .8rem;
	}
</style>