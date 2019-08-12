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

	code,
	kbd,
	pre,
	samp {
		font-family: "SF Mono", "Segoe UI Mono", "Roboto Mono", Menlo, Courier, monospace !important;
		font-size: 1em !important;
		margin: 1em 0px;
	}

	dl dt {
		font-weight: bold;
	}

	dl dd {
		margin: .4rem 0 .8rem 0;
	}

	ul,
	ol {
		margin: .8rem 0 .8rem .8rem;
		padding: 0 !important;
	}

	ul ul,
	ul ol,
	ol ul,
	ol ol {
		margin: .8rem 0 .8rem .8rem;
	}

	ul li,
	ol li {
		margin-top: .4rem;
	}

	ul {
		list-style: disc inside;
	}

	ul ul {
		list-style-type: circle;
	}

	/** Correct the font size and margin on `h1` elements within `section` and `article` contexts in Chrome, Firefox, and Safari. */
	h1 {
		font-size: 2em;
		margin: .67em 0;
	}

	h1,
	h2,
	h3,
	h4,
	h5,
	h6 {
		color: inherit;
		font-weight: 400;
		line-height: 1.2;
		margin-bottom: .5em;
		margin-top: 0;
	}

	.h1,
	.h2,
	.h3,
	.h4,
	.h5,
	.h6 {
		font-weight: 500;
	}

	h1,
	.h1 {
		font-size: 2rem;
	}

	h2,
	.h2 {
		font-size: 1.8rem;
	}

	h3,
	.h3 {
		font-size: 1.6rem;
	}

	h4,
	.h4 {
		font-size: 1.4rem;
	}

	h5,
	.h5 {
		font-size: 1.2rem;
	}

	h6,
	.h6 {
		font-size: 1rem;
	}

	p {
		margin: 0 0 1.2rem;
	}

	.divider {
		display: block;
		position: relative;
		border-top: 1px solid #cccccc;
		height: 1px;
		margin: 2rem 0;
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

	.empty {
		background: transparent !important;
	}

	.json-editor {
		border: 1px solid white;

		.jsoneditor {
			background: white;
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