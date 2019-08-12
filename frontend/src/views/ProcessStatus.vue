<template>
	<div class="process-status" :class="{ 'is-empty': processList && processList.length == 0 && uploadList && uploadList.length == 0 && downloadList && downloadList.length == 0 }" v-if="processList || uploadList || downloadList">
        <EmptyCard v-if="processList && processList.length == 0 && uploadList && uploadList.length == 0 && downloadList && downloadList.length == 0">
            <template v-slot:title>
                Nenhum processo ativo foi encontrado
            </template>
        </EmptyCard>
        <div class="process-wrapper" v-else>
            <div v-if="uploadList && uploadList.length > 0">
                <h3>Uploads</h3>
                <v-list class="uploads">
                    <v-list-item class="list-item" two-line v-for="(process, index) in uploadList" v-bind:key="index">
                        <v-list-item-content class="list-content">
                            <v-list-item-title>
                                <span>{{ process.strat_id }}</span>
                                <v-btn class="ml-2" text small icon @click="removeUploadProcess(process.strat_id)" :disabled="deleting">
                                    <v-icon>mdi-close</v-icon>
                                </v-btn>
                            </v-list-item-title>
                            <v-list-item-subtitle :class="{ 'success--text': process.completed, 'error--text': !process.completed  }">Finalizado: {{ process.completed }}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </div>
            <div v-if="downloadList && downloadList.length > 0">
                <h3>Downloads</h3>
                <v-list class="downloads">
                    <v-list-item class="list-item" two-line v-for="(process, index) in downloadList" v-bind:key="index">
                        <v-list-item-content class="list-content">
                            <v-list-item-title>
                                <span>{{ process.strat_id }}</span>
                                <v-btn class="ml-2" text small icon @click="removeDownloadProcess(process.strat_id)" :disabled="deleting">
                                    <v-icon>mdi-close</v-icon>
                                </v-btn>
                            </v-list-item-title>
                            <v-list-item-subtitle :class="{ 'success--text': process.completed, 'error--text': !process.completed  }">Finalizado: {{ process.completed }}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </div>
            <div v-if="processList && processList.length > 0">
                <h3>Processos em Andamento</h3>
                <v-list class="run-process">
                    <v-list-item class="list-item" two-line v-for="(process, index) in processList" v-bind:key="index">
                        <v-list-item-content class="list-content">
                            <v-list-item-title>
                                Run: {{ process.run_id }} | Strat: {{ process.strat_id }}
                            </v-list-item-title>
                            <v-list-item-subtitle>Tempo: {{ process.start }}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </div>
        </div>
	</div>
	<div class="loading" v-else>
		<v-progress-circular indeterminate :size="100" :width="2"/>
	</div>
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
        private uploadList: any[] | null = null;
        private downloadList: any[] | null = null;
        private calcInterval: any = null;
        private deleting: boolean = false;

        async created() {
            await this.getQueues();
            this.calcInterval = setInterval(async () => this.getQueues(), 5000);
        }

        async getQueues() {
            let processRequests = [
                axios.get('/api/strat/queue'),
                axios.get('/api/strat/get-upload-queue'),
                axios.get('/api/strat/get-download-queue')
            ];

            let [processList, uploadList, downloadList] = await Promise.all(processRequests).then(r => r.map(e => e.data));
            this.processList = processList;
            this.uploadList = uploadList;
            this.downloadList = downloadList;
            
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
        }

        async removeUploadProcess(strat_id) {
            this.deleting = true;
            try {
                let success = await axios.post('/api/strat/remove-upload-queue', {'strat_process_id':strat_id}).then(r => r.data);
                    // .catch(error => {
                    //     if (error.response) {
                    //         console.log(error.response);
                    //     }
                    // });
                this.uploadList = this.uploadList!.filter(e => e.strat_id != strat_id);
				this.$toasted.show('Registro excluído!').goAway(2000);
            } catch (error) {
                // console.error(error);
				this.$toasted.show('Erro ao excluir registro!', {
					type: 'error'
				}).goAway(2000);
            }
            this.deleting = false;
        }

        async removeDownloadProcess(strat_id) {
            this.deleting = true;
            try {
                let success = await axios.post('/api/strat/remove-download-queue', {'strat_process_id':strat_id}).then(r => r.data);
                    // .catch(error => {
                    //     if (error.response) {
                    //         console.log(error.response);
                    //     }
                    // });
                this.downloadList = this.downloadList!.filter(e => e.strat_id != strat_id);
				this.$toasted.show('Registro excluído!').goAway(2000);
            } catch (error) {
                // console.error(error);
				this.$toasted.show('Erro ao excluir registro!', {
					type: 'error'
				}).goAway(2000);
            }
            this.deleting = false;
        }

        beforeDestroy() {
            clearInterval(this.calcInterval);
        }
    }
</script>

<style lang="scss" scoped>
    .run-process,
    .downloads,
    .uploads {
        background: transparent;
        padding: 0 0 15px;
        .list-item {
            width: 50%;
            display: inline-flex;
            padding: 0;
        }
    }
</style>
