<template>
	<div class="process-status" :class="{ 'is-empty': processList && processList.length == 0 && stratProcessList && stratProcessList.length == 0 }" v-if="processList || stratProcessList">
        <EmptyCard v-if="processList && processList.length == 0 && stratProcessList && stratProcessList.length == 0">
            <template v-slot:title>
                Nenhum processo ativo foi encontrado
            </template>
        </EmptyCard>
        <div class="process-wrapper" v-else>
            <div v-if="stratProcessList && stratProcessList.length > 0">
                <h5>Uploads</h5>
                <ul class="strat-process">
                    <li v-for="(process, index) in stratProcessList" v-bind:key="index">
                        <div class="li-wrapper">
                            <div class="li-text">Strat Upload ID: {{ process.name }} | Processando: {{ process.alive }}</div>
                            <button class="btn btn-link btn-sm" @click="removeStratProcess(process.name)"><i class="icon icon-cross"></i></button>
                        </div>
                    </li>
                </ul>
            </div>
            <div v-if="processList && processList.length > 0">
                <h5>Processos em Andamento</h5>
                <ul class="run-process">
                    <li v-for="(process, index) in processList" v-bind:key="index">
                        <div class="li-wrapper">
                            <div class="li-text">
                                Run ID: {{ process.run_id }} | Strat ID: {{ process.strat_id }} | Tempo: {{ process.start }}
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
	</div>
	<div class="loading loading-xlg" v-else></div>
</template>

<script lang="ts">
	import { Component, Vue, Prop } from 'vue-property-decorator';
    import EmptyCard from '@/components/EmptyCard.vue';
    import axios from 'axios';
    import moment from 'moment';
    import _ from 'lodash';
	
	@Component({
        components: {
            EmptyCard
        }
    })
	export default class ProcessStatus extends Vue {
        private processList: any[] | null = null;
        private stratProcessList: any[] | null = null;
        private calcInterval: any = null;

        async created() {
            await this.getQueues();
            this.calcInterval = setInterval(async () => this.getQueues(), 10000);
        }

        async getQueues() {
            let processRequests = [
                axios.get('/api/strat/queue'),
                axios.get('/api/strat/get-upload-queue')
            ];

            let [processList, stratProcessList] = await Promise.all(processRequests).then(r => r.map(e => e.data));
            this.processList = processList;
            this.stratProcessList = stratProcessList;

            this.processList!.forEach(e => {
                if (e.start) {
                    var ms = moment().diff(moment(`${e.start}Z`));
                    var d = moment.duration(ms);
                    var s = Math.floor(d.asHours()).toString().padStart(2, '0') + moment.utc(ms).format(":mm:ss");
                    e.start = s;
                } else {
                    e.start = 'Aguardando';
                }
            });

            // this.processList = (await axios.get('/api/strat/queue')).data;
            // this.processList!.forEach(e => {
            //     if (e.start) {
            //         var ms = moment().diff(moment(`${e.start}Z`));
            //         var d = moment.duration(ms);
            //         var s = Math.floor(d.asHours()).toString().padStart(2, '0') + moment.utc(ms).format(":mm:ss");
            //         e.start = s;
            //     } else {
            //         e.start = 'Aguardando';
            //     }
            // });

            // this.stratProcessList = (await axios.get('/api/strat/get-upload-queue')).data;
        }

        async removeStratProcess(name) {
            try {
                let success = await axios.post('/api/strat/remove-upload-queue', {'strat_process_id':name}).then(r => r.data);
                    // .catch(error => {
                    //     if (error.response) {
                    //         console.log(error.response);
                    //     }
                    // });
                this.stratProcessList = this.stratProcessList.filter(e => e.name != name);
				this.$toasted.show('Registro excluído!').goAway(2000);
            } catch (error) {
                // console.error(error);
				this.$toasted.show('Erro ao excluir registro!', {
					type: 'error'
				}).goAway(2000);
            }
        }

        beforeDestroy() {
            clearInterval(this.calcInterval);
        }
    }
</script>

<style lang="scss" scoped>
    .strat-process,
    .run-process {
        margin-left: 0;
        margin-right: 0;
        list-style: none;
        li {
            margin-top: 15px;
            .li-wrapper {
                display: inline-block;
                padding: 5px 5px 5px 10px;
                box-shadow: 0 0 10px 0px rgba(48, 55, 66, 0.1);
                .li-text,
                button {
                    display: inline-block;
                    vertical-align: middle;
                }
                button {
                    padding: 0 2px;
                    margin: 2px 5px;
                    line-height: 1rem;
                    height: 1.2rem;
                }
            }
        }
    }
</style>
