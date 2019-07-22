<template>
	<div id="app" class="off-canvas off-canvas-sidebar-show">
		<!-- <div id="nav">
			<router-link to="/">Home</router-link> |
			<router-link to="/about">About</router-link>
		</div> -->
		<Sidebar class="off-canvas-sidebar"/>
		<a class="off-canvas-overlay" href="#close"></a>
		<div class="off-canvas-content">
			<div class="container-content">
				<div class="container">
					<a class="off-canvas-toggle btn btn-link btn-action" href="#main-sidebar"><i class="icon icon-menu"></i></a>
					<h3 class="s-title">{{ this.$route.meta.title }}</h3>
					<!-- <p>Nulla duis ex proident esse deserunt id in. Fugiat pariatur sint ex et esse in cillum eu Lorem cillum incididunt. Irure occaecat pariatur laborum minim enim anim laborum minim id ut deserunt id amet elit.</p><p>Irure sint nostrud veniam aliqua velit. Enim laboris ea proident irure irure eiusmod enim eu. Sint proident ex reprehenderit sit culpa minim pariatur minim aliqua fugiat dolore tempor occaecat. Reprehenderit aute adipisicing adipisicing ullamco ut commodo Lorem commodo pariatur. Pariatur tempor id officia voluptate ad ut enim. Veniam Lorem aute nostrud ut commodo magna elit deserunt adipisicing excepteur esse.</p><p>Et duis aliquip occaecat minim proident reprehenderit dolor elit dolor. Aliqua esse minim veniam sunt duis deserunt consequat adipisicing anim aliquip. Pariatur non nulla ullamco mollit culpa pariatur deserunt excepteur consectetur eu occaecat. Laboris do magna adipisicing incididunt et velit do cillum minim laborum. Non labore id aliquip magna aute proident mollit esse voluptate sint nostrud sint in deserunt. Est elit consectetur anim ad ex nisi proident. Est ad ipsum incididunt do labore duis aute cupidatat.</p><p>Ullamco labore ut amet ea adipisicing nisi proident fugiat ad enim sint elit excepteur. Excepteur minim nisi dolore magna quis ad nostrud labore veniam pariatur proident proident. Qui irure sunt deserunt excepteur excepteur irure aliqua. Eu quis qui elit deserunt sint eiusmod eu.</p><p>Excepteur irure dolor ea est aliquip. Pariatur sunt occaecat cupidatat tempor cupidatat velit duis ullamco anim Lorem ad Lorem qui. Ipsum ex et aliqua dolore nisi cillum est dolor nostrud esse veniam aliqua ullamco. Tempor magna Lorem tempor reprehenderit mollit esse dolore adipisicing do reprehenderit proident consectetur dolore officia.</p><p>Consectetur exercitation fugiat ad enim culpa dolore excepteur quis fugiat et id fugiat minim. Ullamco adipisicing veniam occaecat in id Lorem ad deserunt incididunt do consectetur aliqua minim. Sunt labore est nulla do culpa. Veniam excepteur qui dolore deserunt in aliqua adipisicing voluptate duis aliqua proident officia. Ipsum elit consectetur adipisicing consectetur in esse officia incididunt ullamco. Officia esse non duis elit elit labore consequat dolor tempor dolor ipsum mollit. Sunt consequat aliqua occaecat quis tempor enim laboris ad.</p><p>Nulla duis ex proident esse deserunt id in. Fugiat pariatur sint ex et esse in cillum eu Lorem cillum incididunt. Irure occaecat pariatur laborum minim enim anim laborum minim id ut deserunt id amet elit.</p><p>Irure sint nostrud veniam aliqua velit. Enim laboris ea proident irure irure eiusmod enim eu. Sint proident ex reprehenderit sit culpa minim pariatur minim aliqua fugiat dolore tempor occaecat. Reprehenderit aute adipisicing adipisicing ullamco ut commodo Lorem commodo pariatur. Pariatur tempor id officia voluptate ad ut enim. Veniam Lorem aute nostrud ut commodo magna elit deserunt adipisicing excepteur esse.</p><p>Et duis aliquip occaecat minim proident reprehenderit dolor elit dolor. Aliqua esse minim veniam sunt duis deserunt consequat adipisicing anim aliquip. Pariatur non nulla ullamco mollit culpa pariatur deserunt excepteur consectetur eu occaecat. Laboris do magna adipisicing incididunt et velit do cillum minim laborum. Non labore id aliquip magna aute proident mollit esse voluptate sint nostrud sint in deserunt. Est elit consectetur anim ad ex nisi proident. Est ad ipsum incididunt do labore duis aute cupidatat.</p><p>Ullamco labore ut amet ea adipisicing nisi proident fugiat ad enim sint elit excepteur. Excepteur minim nisi dolore magna quis ad nostrud labore veniam pariatur proident proident. Qui irure sunt deserunt excepteur excepteur irure aliqua. Eu quis qui elit deserunt sint eiusmod eu.</p><p>Excepteur irure dolor ea est aliquip. Pariatur sunt occaecat cupidatat tempor cupidatat velit duis ullamco anim Lorem ad Lorem qui. Ipsum ex et aliqua dolore nisi cillum est dolor nostrud esse veniam aliqua ullamco. Tempor magna Lorem tempor reprehenderit mollit esse dolore adipisicing do reprehenderit proident consectetur dolore officia.</p><p>Consectetur exercitation fugiat ad enim culpa dolore excepteur quis fugiat et id fugiat minim. Ullamco adipisicing veniam occaecat in id Lorem ad deserunt incididunt do consectetur aliqua minim. Sunt labore est nulla do culpa. Veniam excepteur qui dolore deserunt in aliqua adipisicing voluptate duis aliqua proident officia. Ipsum elit consectetur adipisicing consectetur in esse officia incididunt ullamco. Officia esse non duis elit elit labore consequat dolor tempor dolor ipsum mollit. Sunt consequat aliqua occaecat quis tempor enim laboris ad.</p><p>Nulla duis ex proident esse deserunt id in. Fugiat pariatur sint ex et esse in cillum eu Lorem cillum incididunt. Irure occaecat pariatur laborum minim enim anim laborum minim id ut deserunt id amet elit.</p><p>Irure sint nostrud veniam aliqua velit. Enim laboris ea proident irure irure eiusmod enim eu. Sint proident ex reprehenderit sit culpa minim pariatur minim aliqua fugiat dolore tempor occaecat. Reprehenderit aute adipisicing adipisicing ullamco ut commodo Lorem commodo pariatur. Pariatur tempor id officia voluptate ad ut enim. Veniam Lorem aute nostrud ut commodo magna elit deserunt adipisicing excepteur esse.</p><p>Et duis aliquip occaecat minim proident reprehenderit dolor elit dolor. Aliqua esse minim veniam sunt duis deserunt consequat adipisicing anim aliquip. Pariatur non nulla ullamco mollit culpa pariatur deserunt excepteur consectetur eu occaecat. Laboris do magna adipisicing incididunt et velit do cillum minim laborum. Non labore id aliquip magna aute proident mollit esse voluptate sint nostrud sint in deserunt. Est elit consectetur anim ad ex nisi proident. Est ad ipsum incididunt do labore duis aute cupidatat.</p><p>Ullamco labore ut amet ea adipisicing nisi proident fugiat ad enim sint elit excepteur. Excepteur minim nisi dolore magna quis ad nostrud labore veniam pariatur proident proident. Qui irure sunt deserunt excepteur excepteur irure aliqua. Eu quis qui elit deserunt sint eiusmod eu.</p><p>Excepteur irure dolor ea est aliquip. Pariatur sunt occaecat cupidatat tempor cupidatat velit duis ullamco anim Lorem ad Lorem qui. Ipsum ex et aliqua dolore nisi cillum est dolor nostrud esse veniam aliqua ullamco. Tempor magna Lorem tempor reprehenderit mollit esse dolore adipisicing do reprehenderit proident consectetur dolore officia.</p><p>Consectetur exercitation fugiat ad enim culpa dolore excepteur quis fugiat et id fugiat minim. Ullamco adipisicing veniam occaecat in id Lorem ad deserunt incididunt do consectetur aliqua minim. Sunt labore est nulla do culpa. Veniam excepteur qui dolore deserunt in aliqua adipisicing voluptate duis aliqua proident officia. Ipsum elit consectetur adipisicing consectetur in esse officia incididunt ullamco. Officia esse non duis elit elit labore consequat dolor tempor dolor ipsum mollit. Sunt consequat aliqua occaecat quis tempor enim laboris ad.</p> -->
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

	// html,
	// body {
	// 	height: 100%;
	// 	margin: 0;
	// }

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

	// #app {
	// 	font-family: 'Avenir', Helvetica, Arial, sans-serif;
	// 	-webkit-font-smoothing: antialiased;
	// 	-moz-osx-font-smoothing: grayscale;
	// 	text-align: center;
	// 	color: #2c3e50;
	// }
	// #nav {
	// 	padding: 30px;
	// 	a {
	// 		font-weight: bold;
	// 		color: #2c3e50;
	// 		&.router-link-exact-active {
	// 			color: #42b983;
	// 		}
	// 	}
	// }
</style>