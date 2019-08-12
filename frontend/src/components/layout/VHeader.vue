<template>
    <v-app-bar app class="header">
        <v-app-bar-nav-icon @click.stop="$emit('input', !value)"></v-app-bar-nav-icon>

        <v-toolbar-title>{{ this.$route.meta.title }}</v-toolbar-title>
        
        <v-spacer></v-spacer>

        <v-btn icon @click="switchTheme">
            <v-icon>mdi-invert-colors</v-icon>
        </v-btn>
    </v-app-bar>
</template>

<script lang="ts">
    import { Component, Vue, Prop } from 'vue-property-decorator';
    
    @Component({})
	export default class VHeader extends Vue {
        @Prop() value!: boolean;

        mounted() {
            if (JSON.parse(localStorage.darkTheme)) (<any>this).$vuetify.theme.dark = true;
            else (<any>this).$vuetify.theme.dark = false;
        }
        
        switchTheme() {
            (<any>this).$vuetify.theme.dark = !(<any>this).$vuetify.theme.dark;
            localStorage.darkTheme = (<any>this).$vuetify.theme.dark;
        }
    }
</script>

<style lang="scss" scoped>
    
</style>


