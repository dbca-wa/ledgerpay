<template lang="html">
    <div v-if="ledgerpay" class="container" id="internalAssessment">
      <div class="row">
        <!--h3>Entry Legder Pay Request: {{ ledgerpay.lodgement_number }}</h3-->
        <h3>{{ assessmentTitle }}</h3>
        <div class="col-md-3">
            <CommsLogs :comms_url="comms_url" :logs_url="logs_url" :comms_add_url="comms_add_url" :disable_add_entry="false"/>

            <div class="row">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        Workflow
                    </div>
                    <div class="panel-body panel-collapse">
                        <div class="row">
                            <div class="col-sm-12">
                                <strong>Status</strong><br/>
                                {{ ledgerpay.processing_status }}
                            </div>
                            <div class="col-sm-12">
                                <div class="separator"></div>
                            </div>

                            <div class="col-sm-12 top-buffer-s">
                                <strong>Currently assigned to</strong><br/>
                                <div class="form-group">
                                    <template>
                                        <select ref="assigned_officer" :disabled="!canAssign" class="form-control" v-model="ledgerpay.assigned_officer_id">
                                            <option :value="null"></option>
                                            <option v-for="member in ledgerpay.action_group" :value="member.id">{{member.first_name}} {{member.last_name}}</option>
                                        </select>
                                        <a v-if="canAssign && ledgerpay.assigned_officer != ledgerpay.current_officer.id" @click.prevent="assignRequestUser()" class="actionBtn pull-right">Assign to me</a>
                                    </template>
                                </div>
                            </div>

                            <div class="col-sm-12 top-buffer-s" v-if="!isFinalised && canProcess">
                                <div v-if="show_spinner"><i class='fa fa-5x fa-spinner fa-spin'></i></div>
                                <div v-else>
                                <template v-if="canProcessAssessor">
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <strong>Action</strong><br/>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <button style="width:80%;" class="btn btn-primary" :disabled="allVisitsUnchecked" @click.prevent="workflowAction('propose_issue')">Propose Issue Legder Pay</button><br/>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <button style="width:80%;" class="btn btn-primary top-buffer-s" :disabled="allVisitsUnchecked" @click.prevent="workflowAction('propose_concession')">Propose Issue Concession</button><br/>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <button style="width:80%;" class="btn btn-primary top-buffer-s" :disabled="false" @click.prevent="workflowAction('propose_decline')">Propose Decline</button><br/>
                                        </div>
                                    </div>
                                </template>
                                <template v-if="canProcessApprover">
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <button style="width:80%;" class="btn btn-primary top-buffer-s" :disabled="false" @click.prevent="workflowAction('return_to_assessor')">Return to Assessor</button><br/>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <button style="width:80%;" class="btn btn-primary top-buffer-s" :disabled="allVisitsUnchecked" @click.prevent="finalApproval('issue')">Issue Legder Pay</button><br/>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <button style="width:80%;" class="btn btn-primary top-buffer-s" :disabled="allVisitsUnchecked" @click.prevent="finalApproval('issue_concession')">Issue Concession</button><br/>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <button style="width:80%;" class="btn btn-primary top-buffer-s" :disabled="false" @click.prevent="finalApproval('decline')">Decline</button><br/>
                                        </div>
                                    </div>
                                </template>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-1"></div>
        <div class="col-md-8">
            <div v-if="ledgerPayId" class="row">
                <LedgerPayForm
                :ledgerPayId="ledgerPayId"
                 ref="ledger_pay_form"
                :key="ledgerPayId"
                 :isInternal="true"
                 :canProcess="canProcess"
                 :isFinalised="isFinalised"
                 @all-visits-unchecked="updateVisits"
                />
            </div>
        </div>
        </div>
        <div v-if="workflowActionType">
            <AssessmentWorkflow ref="assessment_workflow" :ledgerpay="ledgerpay" :workflow_type="workflowActionType" :key="'workflow_action_' + workflowActionType"/>
        </div>
    </div>
</template>
<script>
import CommsLogs from '@common-utils/comms_logs.vue'
import { api_endpoints, helpers } from '@/utils/hooks'
import LedgerPayForm from '../ledgerpay_form.vue'
import Vue from 'vue'
import AssessmentWorkflow from './assessment_modal.vue'


export default {
    name: 'Assessment',
    data: function() {
        let vm = this;
        return {
            allVisitsUnchecked: true,
            ledgerPayId: null,
            ledgerpay: {},
            show_spinner: false,
            workflowActionType: '',
            detailsBody: 'detailsBody'+vm._uid,
            addressBody: 'addressBody'+vm._uid,
            contactsBody: 'contactsBody'+vm._uid,
            siteLocations: 'siteLocations'+vm._uid,
            defaultKey: "aho",
            "ledgerpay": null,
            "original_ledgerpay": null,
            "loading": [],
            selected_referral: '',
            referral_text: '',
            approver_comment: '',
            form: null,
            members: [],
            //department_users : [],
            contacts_table_initialised: false,
            initialisedSelects: false,
            showingProposal:false,
            showingRequirements:false,
            hasAmendmentRequest: false,
            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            comms_url: helpers.add_endpoint_json('/api/ledgerpays',vm.$route.params.ledger_pay_id+'/comms_log'),
            comms_add_url: helpers.add_endpoint_json('/api/ledgerpays',vm.$route.params.ledger_pay_id+'/add_comms_log'),
            logs_url: helpers.add_endpoint_json('/api/ledgerpays',vm.$route.params.ledger_pay_id+'/action_log'),
            panelClickersInitialised: false,
        }
    },
    components: {
        CommsLogs,
        LedgerPayForm,
        AssessmentWorkflow,
    },
    filters: {
        formatDate: function(data){
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss'): '';
        }
    },
    props: {
    },
    watch: {

    },
    computed: {
        assessmentTitle: function() {
            let title = 'Entry Legder Pay Request: ' + this.ledgerpay.lodgement_number;
            if (this.ledgerpay && this.ledgerpay.proposed_status && this.ledgerpay.processing_status === "With Approver") {
                switch (this.ledgerpay.proposed_status) {
                    case "Decline":
                        title += ' (Proposed Decision: Decline)';
                        break;
                    case "Legder Pay":
                        title += ' (Proposed Decision: Issue Legder Pay)';
                        break;
                    case "Concession":
                        title += ' (Proposed Decision: Issue Concession)';
                        break;
                }
            }
            return title;
        },
        ledgerpay_form_url: function() {
        },
        canProcess: function() {
            let process = false;
            if (this.ledgerpay && this.ledgerpay.can_process) {
                process = true;
            }
            return process;
        },
        canAssign: function() {
            let assign = false;
            if (this.ledgerpay && this.ledgerpay.can_assign) {
                assign = true;
            }
            return assign;
        },
        canProcessAssessor: function() {
            let canProcess = false;
            if (this.ledgerpay.processing_status === 'With Assessor' && this.ledgerpay.can_process) {
                canProcess = true;
            }
            return canProcess;
        },
        canProcessApprover: function() {
            let canProcess = false;
            if (this.ledgerpay.processing_status === 'With Approver' && this.ledgerpay.can_process) {
                canProcess = true;
            }
            return canProcess;
        },
        isFinalised: function(){
            return this.ledgerpay.processing_status == 'Declined' || this.ledgerpay.processing_status == 'Issued';
        },
    },
    methods: {
        updateVisits: function(val) {
            this.allVisitsUnchecked = val;
        },
        commaToNewline(s){
            return s.replace(/[,;]/g, '\n');
        },
        finalApproval: async function(approval_type) {
          this.show_spinner = true;
          let post_url = '/api/ledgerpays/' + this.ledgerpay.id + '/final_approval/'
          let payload = {"approval_type": approval_type}
          let ledgerPayRes = await this.parentSave(false)
          if (ledgerPayRes.ok) {
              try {
                  let res = await Vue.http.post(post_url, payload);
                  if (res.ok) {    
                      this.$router.push({
                          name: 'ledger-pay-dash',
                      });
                  }
              } catch(err) {
                  this.errorResponse = 'Error:' + err.statusText;
              } 
          } else {
              this.errorResponse = 'Error:' + ledgerPayRes.statusText;
          }
          this.show_spinner = false;
      },
        updateAssignedOfficerSelect:function(){
            let vm = this;
            $(vm.$refs.assigned_officer).val(vm.ledgerpay.assigned_officer_id);
            $(vm.$refs.assigned_officer).trigger('change');
        },
        /*
        assignRequestUser: function(){
            let vm = this;
            vm.$http.get(helpers.add_endpoint_json('/api/ledgerpays',(vm.ledgerpay.id+'/assign_request_user')))
            .then((response) => {
                vm.ledgerpay = response.body;
                //vm.updateAssignedOfficerSelect();
            }, (error) => {
                //vm.updateAssignedOfficerSelect();
                swal(
                    'Proposal Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });
        },
        */
        assignRequestUser: async function(){
            await this.$nextTick();
            const res = await this.$http.get(helpers.add_endpoint_json('/api/ledgerpays',(this.ledgerpay.id+'/assign_request_user')))
            this.ledgerpay = res.body;
            await this.$nextTick();
            this.updateAssignedOfficerSelect();
        },
        assignTo: async function() {
            await this.$nextTick();
            const data = {'assigned_officer_id': this.ledgerpay.assigned_officer_id};
            const res = await this.$http.post(helpers.add_endpoint_json('/api/ledgerpays',(this.ledgerpay.id+'/assign_to')),data);
            this.ledgerpay = res.body;
            await this.$nextTick();
            this.updateAssignedOfficerSelect();
        },
        unAssign: async function() {
            await this.$nextTick();
            const res = await this.$http.get(helpers.add_endpoint_json('/api/ledgerpays',(this.ledgerpay.id+'/unassign')))
            this.ledgerpay = res.body;
            await this.$nextTick();
            this.updateAssignedOfficerSelect();
        },
        /*
        assignTo: function(){
            let vm = this;
            let unassign = true;
            let data = {};
            unassign = vm.ledgerpay.assigned_officer != null ? false: true;
            data = {'assigned_officer_id': vm.ledgerpay.assigned_officer};
            if (!unassign){
                vm.$http.post(helpers.add_endpoint_json('/api/ledgerpays',(vm.ledgerpay.id+'/assign_to')),JSON.stringify(data),{
                    emulateJSON:true
                }).then((response) => {
                    vm.ledgerpay = response.body;
                    //vm.updateAssignedOfficerSelect();
                }, (error) => {
                    //vm.updateAssignedOfficerSelect();
                    swal(
                        'Proposal Error',
                        helpers.apiVueResourceError(error),
                        'error'
                    )
                });
            }
            else{
                vm.$http.get(helpers.add_endpoint_json('/api/ledgerpays',(vm.ledgerpay.id+'/unassign')))
                .then((response) => {
                    vm.ledgerpay = response.body;
                    //vm.updateAssignedOfficerSelect();
                }, (error) => {
                    //vm.updateAssignedOfficerSelect();
                    swal(
                        'Proposal Error',
                        helpers.apiVueResourceError(error),
                        'error'
                    )
                });
            }
        },
        */
        parentSave: async function() {
            const ledgerPayRes = await this.$refs.ledger_paledger_paym.save(false);
            return ledgerPayRes;
        },
        workflowAction: function(action) {
            this.workflowActionType = action;
            this.$nextTick(() => {
                this.$refs.assessment_workflow.isModalOpen = true;
            });
        },

        initialiseAssignedOfficerSelect:function(reinit=false){
            let vm = this;
            if (reinit){
                $(vm.$refs.assigned_officer).data('select2') ? $(vm.$refs.assigned_officer).select2('destroy'): '';
            }
            // Assigned officer select
            $(vm.$refs.assigned_officer).select2({
                "theme": "bootstrap",
                allowClear: true,
                placeholder:"Select Officer"
            }).
            on("select2:select", async function (e) {
                var selected = $(e.currentTarget);
                vm.ledgerpay.assigned_officer_id = selected.val();
                //await vm.$nextTick();
                await vm.assignTo();
                /*
            }).on("select2:unselecting", function(e) {
                var self = $(this);
                setTimeout(() => {
                    self.select2('close');
                }, 0);
                */
            }).on("select2:unselect", async function (e) {
                var selected = $(e.currentTarget);
                vm.ledgerpay.assigned_officer_id = null;
                //await vm.$nextTick();
                await vm.unAssign();
            });
            //});
        },


    },
    created: async function() {
        await this.$nextTick();
        const res = await Vue.http.get(`/api/ledgerpays/${this.ledgerpayId}.json`)
        this.ledgerpay = res.body;
        await this.$nextTick();
        this.initialiseAssignedOfficerSelect()
    },
    /*
    updated: function(){
        this.$nextTick(() => {
            this.initialiseAssignedOfficerSelect()
        });
    },
    mounted: async function() {
        await this.$nextTick();
        //this.$nextTick(() => {
        //this.initialiseAssignedOfficerSelect()
        //this.updateAssignedOfficerSelect()
        //});
    },
    */
    beforeRouteEnter: function(to, from, next) {
        next(vm => {
            vm.ledgerPayId = to.params.ledger_pay_id;
        })
    }
}
</script>
<style scoped>
.top-buffer-s {
    margin-top: 10px;
}
.actionBtn {
    cursor: pointer;
}
.hidePopover {
    display: none;
}
.separator {
    border: 1px solid;
    margin-top: 15px;
    margin-bottom: 10px;
    width: 100%;
}
</style>
