<template>
    <v-card v-page-title="pageTitle">
        <v-card-title>{{ $t('Submit thesis') }}</v-card-title>
        <v-form @submit.prevent="submit" ref="form" v-model="valid">
            <v-card-text>
                <v-row>
                    <v-col cols="12" lg="6">
                        <v-text-field
                            disabled filled v-model="thesis.title"
                            :label="$t('Thesis title')"
                        ></v-text-field>
                        <v-text-field
                            disabled filled :value="(new Date(thesis.submit_deadline)).toLocaleDateString($i18n.locale)"
                            :label="$t('Submit deadline')"
                        ></v-text-field>

                        <v-textarea
                            outlined hide-details
                            rows="15" class="mb-5" autofocus
                            :label="$t('Abstract')"
                            v-model="thesis.abstract"
                            :rules="[v => !!v]"
                        ></v-textarea>

                        <v-checkbox
                            :label="$t('Approved publication and borrowing')"
                            :hint="$t('thesis.reservableHint')"
                            v-model="thesis.reservable"
                            persistent-hint :true-value="true" :false-value="false" class="mb-5"
                        ></v-checkbox>
                    </v-col>
                    <v-col cols="12" lg="6">
                        <v-combobox
                            :label="$t('Keywords')" prepend-icon="mdi-format-letter-starts-with"
                            chips clearable v-model="thesis.keywords" multiple outlined
                            :delimiters="', '.split('')"
                        >
                            <!--    TODO: save keywords -->
                            <template v-slot:selection="{ attrs, item, select, selected }">
                                <v-chip
                                    v-bind="attrs"
                                    :input-value="selected"
                                    close @click="select" @click:close="removeKeyWord(item)"
                                >
                                    <strong>{{ item }}</strong>
                                </v-chip>
                            </template>
                        </v-combobox>

                        <v-file-input
                            :label="$t('Thesis text')"
                            v-model="thesis.thesisText"
                            :rules="[v => !!v]"
                            :accept="typeAttachmentAcceptTypes('thesis_text')"
                            prepend-icon="$thesis_text"
                        ></v-file-input>

                        <v-file-input
                            :label="$t('Thesis poster')"
                            v-model="thesis.thesisPoster"
                            :accept="typeAttachmentAcceptTypes('thesis_poster')"
                            prepend-icon="$thesis_poster"
                        ></v-file-input>

                        <v-file-input
                            :label="$t('Thesis attachment')"
                            v-model="thesis.thesisAttachment"
                            :accept="typeAttachmentAcceptTypes('thesis_attachment')"
                            prepend-icon="$thesis_attachment"
                        ></v-file-input>

                        <v-divider></v-divider>
                        <v-row no-gutters>
                            <v-col v-for="(hintsChunk, i) in submitHints" :key="i" class="d-flex flex-column px-5">
                                <v-switch
                                    v-for="(label, i) in hintsChunk" :key="i"
                                    :rules="[v => !!v]" :label="label"
                                    inset color="success"
                                >
                                </v-switch>
                            </v-col>
                        </v-row>

                        <v-alert
                            v-if="errorMessages.length" type="warning"
                            v-for="message in errorMessages" v-text="message" :key="message">
                        </v-alert>
                    </v-col>
                </v-row>


            </v-card-text>

            <v-divider></v-divider>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn type="submit" color="success" :disabled="!valid" x-large>
                    {{ $t('Submit thesis') }}
                </v-btn>
            </v-card-actions>
        </v-form>
    </v-card>
</template>

<script type="text/tsx">
    import _ from 'lodash';
    import Vue from 'vue';
    import Axios from '../../axios';
    import {OPTIONS_ACTIONS} from '../../store/options';
    import {optionsStore} from '../../store/store';
    import {notificationBus, readFileAsync} from '../../utils';

    export default Vue.extend({
        name: 'SubmitForm',
        props: {
            id: {type: String, required: true}
        },
        data() {
            return {
                valid: false,
                errorMessages: [],
                thesis: {
                    abstract: '',
                    reservable: true,
                    thesisText: null,
                    thesisPoster: null,
                    thesisAttachment: null,
                    keywords: []
                }
            };
        },
        computed: {
            ...optionsStore.mapGetters(['typeAttachmentAcceptTypes']),
            submitHints() {
                return _.chunk([
                    this.$t('thesis.submit.hintAdmission'),
                    this.$t('thesis.submit.hintAttachment'),
                    this.$t('thesis.submit.hintPoster'),
                    this.$t('thesis.submit.hintThesisFinal'),

                    this.$t('thesis.submit.hintAbstractSame'),
                    this.$t('thesis.submit.hintSubmitApprove')
                ], 4);
            },
            pageTitle() {
                return `${this.$t('page.title.thesisSubmit')} ${this.thesis.title}`;
            }
        },
        methods: {
            ...optionsStore.mapActions([OPTIONS_ACTIONS.LOAD_OPTIONS]),
            async submit() {
                let formData = new FormData();

                const data = {
                    ...this.thesis,
                    thesisText: undefined
                };
                if (!this.thesis.thesisText) {
                    this.valid = false;
                    return;
                }
                data.thesisText = await readFileAsync(this.thesis.thesisText);
                if (this.thesis.thesisPoster)
                    data.thesisPoster = await readFileAsync(this.thesis.thesisPoster);
                if (this.thesis.thesisAttachment)
                    data.thesisPoster = await readFileAsync(this.thesis.thesisAttachment);

                for (let key in data) {
                    formData.append(key, this.thesis[key]);
                }
                const resp = await Axios.patch(`/api/v1/thesis/${this.id}/submit`, formData, {
                    headers: {'Content-Type': 'multipart/form-data'}
                });

                if (resp.data.id) {
                    notificationBus.success(this.$t('thesis.justSubmitted'));
                    await this.$router.push({name: 'dashboard'});
                } else {
                    this.errorMessages = resp.data;
                    this.valid = false;
                }
            },
            removeKeyWord(item) {
                this.thesis.keywords.splice(this.thesis.keywords.indexOf(item), 1);
                this.thesis.keywords = [...this.thesis.keywords];
            }
        },
        async created() {
            this.thesis = (await Axios.get(`/api/v1/thesis/${this.id}`)).data;
            this.$watch('thesis', (old, new_) => {
                if (!this.valid)
                    this.valid = true;
            }, {deep: true});
            await this[OPTIONS_ACTIONS.LOAD_OPTIONS]();
        }
    });
</script>

<style scoped>

</style>