<template>
	<div id="app" class="off-canvas off-canvas-sidebar-show">
		<Sidebar class="off-canvas-sidebar"/>
		<a class="off-canvas-overlay" href="#close"></a>
		<div class="off-canvas-content">
			<div class="container-content">
				<div class="container">
					<a class="off-canvas-toggle btn btn-link btn-action" href="#main-sidebar"><i class="icon icon-menu"></i></a>
					<h3 class="s-title">{{ this.$route.meta.title }}</h3>
					<router-view/>
				</div>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import Sidebar from '@/components/layout/Sidebar.vue';

	@Component({
		components: {
			Sidebar
		},
	})
	export default class App extends Vue { }
</script>

<style lang="scss">
	@import url('https://fonts.googleapis.com/css?family=Roboto&display=swap');
	@import '~spectre.css/dist/spectre.min.css';
	@import '~spectre.css/dist/spectre-icons.min.css';
	@import '~spectre.css/dist/spectre-exp.min.css';

	body {
		font-family: 'Roboto', sans-serif;
	}

	.off-canvas-toggle {
		left: 15px !important;
		top: 20px !important;
	}

    .off-canvas-sidebar {
        padding: 20px 1rem;
        height: 100vh;
        overflow-y: auto;
    }

	.off-canvas-content {
		padding: 0 !important;
	}

	.container-content {		
		flex: 1 1 auto;
		padding: 0 4rem;
		// width: calc(100vw - 12rem);
		height: 100vh;
		overflow-y: auto;

		@media (max-width: 960px) {
    		padding: 0 50px;
		}
	}

	.s-title {
		position: sticky;
		position: -webkit-sticky;
		top: 0;
		z-index: 99;
		padding: 20px 0;
		margin: 0;
		background: white;
	}

	.form-horizontal {
		.form-group {
			margin-bottom: 20px !important;
			& > :nth-child(even),
			& > .col-ml-auto:only-child {
				padding-left: 20px;
			}
		}
	}

	.json-editor {
		min-height: 150px;
	}
</style>