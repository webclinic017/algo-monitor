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
	import Toasted from 'vue-toasted';
	
	Vue.use(Toasted);
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
	@import '~vue-good-table/dist/vue-good-table.css';

	body {
		font-family: 'Roboto', sans-serif;
	}

	.subtitle {
		color: #707070;
	}

	.off-canvas {
		.off-canvas-sidebar {
			padding: 20px 1rem;
			height: 100vh;
			overflow-y: auto;
		}

		.off-canvas-content {
			padding: 0 !important;
			overflow-x: hidden;

			.container-content {		
				flex: 1 1 auto;
				padding: 0 60px 60px;
				height: 100vh;
				overflow-y: auto;

				@media (max-width: 960px) {
					padding: 0 50px 50px;
				}

				.container {
					min-height: 100%;
					display: flex;
					flex-direction: column;

					&>div.is-empty:only-of-type,
					&>div.loading:only-of-type {
						flex: 1;
						display: flex;
						flex-direction: column;
						justify-content: space-around;
						margin-bottom: 5%;
					}
					
					.off-canvas-toggle {
						left: 15px !important;
						top: 20px !important;
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
				}
			}
		}
	}

	.empty {
		background: transparent !important;
	}

	.form-horizontal {
		&:last-child {
			padding: 0;
		}
		.form-group {
			&:not(:last-child) {
				margin-bottom: 20px !important;
			}
			& > :nth-child(even),
			& > .col-ml-auto:only-child {
				padding-left: 20px;
			}
		}
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

	.vgt-table {
		thead {
			user-select: none;
			cursor: pointer;
		}
	}


	.jsoneditor-contextmenu ul li button {
		color: #f5f5f5 !important;
		&:hover {
			color: #1a1a1a !important;
		}
	}

	.loading.loading-xlg {
		min-height: 100px;
		&::after {
			height: 80px;
			margin-left: -40px;
			margin-top: -40px;
			width: 80px;
		}
	}

	.disable-events {
		pointer-events: none;
	}
</style>