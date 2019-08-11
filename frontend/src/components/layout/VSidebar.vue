<template>
    <v-navigation-drawer app class="sidebar" :value="value" @input="$emit('input', $event)">
        <v-list-item>
            <v-list-item-content>
                <v-list-item-title class="title">
                    Algo Monitor
                    <span class="logo">
                        <v-img src="@/assets/bar-chart.png" alt="Logo"/>
                    </span>
                </v-list-item-title>
                <!-- <v-list-item-subtitle>
                    subtext
                </v-list-item-subtitle> -->
            </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>
        
        <v-list dense nav>
            <v-list-item link :to="{name:'home'}" exact>
                <v-list-item-content>
                    <v-list-item-title>Home</v-list-item-title>
                </v-list-item-content>
            </v-list-item>

            <v-list-item link :to="{name:'results'}" exact>
                <v-list-item-content>
                    <v-list-item-title>Resultados</v-list-item-title>
                </v-list-item-content>
            </v-list-item>

            <v-list-item link :to="{name:'process'}" exact>
                <v-list-item-content>
                    <v-list-item-title>Processos</v-list-item-title>
                </v-list-item-content>
            </v-list-item>

            <v-list-group no-action value="true">
                <template v-slot:activator>
                    <v-list-item-title>Estratégias</v-list-item-title>
                </template>
                
                <v-list-item link :to="{name:'strat-run'}" exact>
                    <v-list-item-content>
                        <v-list-item-title>Executar</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link :to="{name:'strat-create'}" exact>
                    <v-list-item-content>
                        <v-list-item-title>Criar</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link :to="{name:'strat-list'}" exact>
                    <v-list-item-content>
                        <v-list-item-title>Listar</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list-group>
        </v-list>
    </v-navigation-drawer>
</template>

<script lang="ts">
    import { Component, Vue, Prop } from 'vue-property-decorator';
    
    @Component({})
	export default class VSidebar extends Vue {
        @Prop() value!: boolean;
    }
</script>

<style lang="scss" scoped>
    .logo {
        display: inline-block;
        width: 25px;
        margin-left: 10px;
    }
</style>


