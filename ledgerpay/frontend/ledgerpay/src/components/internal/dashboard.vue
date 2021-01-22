<template id="proposal_dashboard">
    <div class="container">
        <!--
        <FormSection :formCollapse="false" label="Ledger Pay Requests" Index="ledger_pay_requests">
            <div class="row">
                <div class="col-md-3">
                    <label for="">Lodged From</label>
                    <div class="input-group date" ref="ledgerpayDateFromPicker">
                        <input type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="filterLedgerPayLodgedFrom">
                        <span class="input-group-addon">
                            <span class="glyphicon glyphicon-calendar"></span>
                        </span>
                    </div>
                </div>
                <div class="col-md-3">
                    <label for="">Lodged To</label>
                    <div class="input-group date" ref="ledgerpayDateToPicker">
                        <input type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="filterLedgerPayLodgedTo">
                        <span class="input-group-addon">
                            <span class="glyphicon glyphicon-calendar"></span>
                        </span>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label for="">Status</label>
                        <select class="form-control" v-model="filterLedgerPayStatus">
                            <option value="All">All</option>
                            <option v-for="s in ledgerpay_status" :value="s">{{s}}</option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-lg-12" style="margin-top:25px;">
                    <datatable ref="ledgerpay_datatable" :id="datatable_id" :dtOptions="ledgerpay_options" :dtHeaders="ledgerpay_headers"/>
                </div>
            </div>
        </FormSection>
        -->
        </div>
</template>
<script>

import datatable from '@/utils/vue/datatable.vue'
import Vue from 'vue'
import FormSection from "@/components/forms/section_toggle.vue"
import ResponsiveDatatablesHelper from "@/utils/responsive_datatable_helper.js"
import {
    api_endpoints,
    helpers
}from '@/utils/hooks'
export default {
    name: 'LedgerPayDash',
    props: {
    },
    data() {
        let vm = this;
        return {
            url: '/api/ledgerpays_paginated/ledgerpay_internal/?format=datatables',
            pBody: 'pBody' + vm._uid,
            datatable_id: 'ledgerpay-datatable-'+vm._uid,
            show_spinner: false,
            filterLedgerPayStatus: 'All',
            filterLedgerPayLodgedFrom: '',
            filterLedgerPayLodgedTo: '',
            dashboardTitle: '',
            dashboardDescription: '',
            dateFormat: 'DD/MM/YYYY',
            datepickerOptions:{
                format: 'DD/MM/YYYY',
                showClear:true,
                useCurrent:false,
                keepInvalid:true,
                allowInputToggle:true
            },
            ledgerpay_status:[],
            ledgerpay_headers:["Lodgement Number", "Organisation", "Status", "Lodged on", "Document", "Assigned To", "", "", "Action", "Participant", "Comments to applicant"],
            ledgerpay_options:{
                language: {
                    processing: "<i class='fa fa-4x fa-spinner fa-spin'></i>"
                },
                responsive: true,
                serverSide: true,
                order: [
                    [0, 'desc']
                    ],
                ajax: {
                    "url": '/api/ledgerpays_paginated/ledgerpay_internal/?format=datatables',
                    "dataSrc": 'data',
                    // adding extra GET params for Custom filtering
                    "data": function ( d ) {
                        d.date_from = vm.filterLedgerPayLodgedFrom != '' && vm.filterLedgerPayLodgedFrom != null ? moment(vm.filterLedgerPayLodgedFrom, 'DD/MM/YYYY').format('YYYY-MM-DD'): '';
                        d.date_to = vm.filterLedgerPayLodgedTo != '' && vm.filterLedgerPayLodgedTo != null ? moment(vm.filterLedgerPayLodgedTo, 'DD/MM/YYYY').format('YYYY-MM-DD'): '';
                        d.processing_status = vm.filterLedgerPayStatus;
                    }

                },
                dom: 'lBfrtip',
                buttons:[
                    {
                        extend: 'excel',
                        exportOptions: {
                            columns: ':visible'
                        }
                    },
                    {
                        extend: 'csv',
                        exportOptions: {
                            columns: ':visible'
                        }
                    },
                ],
                columns: [
                    {
                        data: "lodgement_number",
                        visible: true,
                        //searchable: false,
                    },
                    {
                        data: "organisation",
                        visible: true,
                        orderable: false,
                    },
                    {
                        data: "processing_status",
                        mRender:function (data,type,full) {
                            let fullStatus = full.processing_status;
                            return fullStatus
                        },
                        //searchable: false,
                        visible: true,
                    },
                    {
                        data: "lodgement_date",
                        mRender:function (data,type,full) {
                            return data != '' && data != null ? moment(data).format(vm.dateFormat): '';
                        },
                        visible: true,
                    },
                    {
                        data: "latest_ledgerpay_document",
                        visible: true,
                        orderable: false,
                        mRender:function(data,type,full){
                            if (data) {
                                return `<a href="${data}" target="_blank"><i style="color:red" class="fa fa-file-pdf-o"></i></a>`;
                            } else {
                                return null;
                            }
                        },

                        //searchable: false,
                    },
                    {
                        data: "assigned_officer",
                        visible: true,
                        //searchable: false,
                    },
                    {
                        data: "proposed_status",
                        visible: false,
                        //searchable: false,
                    },
                    {
                        data: "action_shortcut",
                        visible: false,
                        //searchable: false,
                    },
                    {
                        data: "can_process",
                        mRender:function (data,type,full) {
                            //let links = '';
                            let links = full.action_shortcut;
                            if(full.can_process){

                                links +=  `<a href='/internal/ledger_pay/${full.id}'>Process</a><br/>`;
                            } else{
                                links +=  `<a href='/internal/ledger_pay/${full.id}'>View</a><br/>`;
                            }
                            return links;
                        },
                        name: '',
                        searchable: false,
                        orderable: false
                    },
                    {
                        data: "participants",
                        visible: true,
                        orderable: false,
                    },
                    {
                        data: "comments_to_applicant",
                        visible: true,
                        mRender: function (value) {
                            var ellipsis = '...',
                                truncated = _.truncate(value, {
                                    length: 25,
                                    omission: ellipsis,
                                    separator: ' '
                                }),
                                result = '<span>' + truncated + '</span>',
                                popTemplate = _.template('<a href="#" ' +
                                //popTemplate = _.template('<button ' +
                                    'role="button" ' +
                                    'data-toggle="popover" ' +
                                    'data-trigger="click" ' +
                                    'data-placement="top auto"' +
                                    'data-html="true" ' +
                                    'data-container="body" ' +
                                    'data-content="<%= text %>" ' +
                                    '>more</a>');
                            if (_.endsWith(truncated, ellipsis)) {
                                result += popTemplate({
                                    text: value
                                });
                            }

                            return result;
                        },

                        'createdCell': function (cell) {
                            //TODO why this is not working?
                            // the call to popover is done in the 'draw' event
                            $(cell).popover();
                        }
                        //responsivePriority: 50,
                        //width: "50%",
                        //searchable: false,
                    },
                    {
                        data: "id",
                        visible: false,
                        orderable: false,
                    },


                ],
                processing: true,
                initComplete: function() {
                    vm.$refs.ledgerpay_datatable.vmDataTable.columns.adjust().draw();
                },
            }
        }
    },
    components:{
        FormSection,
        datatable,
    },
    watch:{
        filterLedgerPayStatus: function(){
            this.$refs.ledgerpay_datatable.vmDataTable.draw();
        },

        filterLedgerPayLodgedFrom: function(){
            this.$refs.ledgerpay_datatable.vmDataTable.draw();
        },
        filterLedgerPayLodgedTo: function(){
            this.$refs.ledgerpay_datatable.vmDataTable.draw();
        }
    },
    computed: {
    },
    methods:{
        fetchFilterLists: function(){
            let vm = this;

            vm.$http.get(api_endpoints.filter_list).then((response) => {
                vm.ledgerpay_status = response.body.ledgerpay_status_choices;
            },(error) => {
            })
        },
        actionShortcut: async function(id, approvalType) {
            let vm = this;
            let processingTableStr = `.action-${id}`;
            let processingTable = $(processingTableStr);
            processingTable.replaceWith("<div><i class='fa fa-2x fa-spinner fa-spin'></i></div>");
            let post_url = '/api/ledgerpays/' + id + '/final_approval/'
            let res = await Vue.http.post(post_url, {'approval_type': approvalType});
            if (res.ok) {
                this.refreshFromResponse();
            }
        },
        refreshFromResponse: function(){
            this.$refs.ledgerpay_datatable.vmDataTable.ajax.reload();
        },
        addEventListeners: function(){
            let vm = this;
            // Initialise Proposal Date Filters
            $(vm.$refs.ledgerpayDateToPicker).datetimepicker(vm.datepickerOptions);
            $(vm.$refs.ledgerpayDateToPicker).on('dp.change', function(e){
                if ($(vm.$refs.ledgerpayDateToPicker).data('DateTimePicker').date()) {
                    vm.filterLedgerPayLodgedTo =  e.date.format('DD/MM/YYYY');
                }
                else if ($(vm.$refs.ledgerpayDateToPicker).data('date') === "") {
                    vm.filterLedgerPayLodgedTo = "";
                }
             });
            $(vm.$refs.ledgerpayDateFromPicker).datetimepicker(vm.datepickerOptions);
            $(vm.$refs.ledgerpayDateFromPicker).on('dp.change',function (e) {
                if ($(vm.$refs.ledgerpayDateFromPicker).data('DateTimePicker').date()) {
                    vm.filterLedgerPayLodgedFrom = e.date.format('DD/MM/YYYY');
                    $(vm.$refs.ledgerpayDateToPicker).data("DateTimePicker").minDate(e.date);
                }
                else if ($(vm.$refs.ledgerpayDateFromPicker).data('date') === "") {
                    vm.filterLedgerPayLodgedFrom = "";
                }
            });
            //Internal Action shortcut listeners
            let table = vm.$refs.ledgerpay_datatable.vmDataTable
            table.on('processing.dt', function(e) {
            })
            table.on('click', 'a[data-issue]', async function(e) {
                e.preventDefault();
                var id = $(this).attr('data-issue');
                await vm.actionShortcut(id, 'issue');
            }).on('click', 'a[data-concession]', async function(e) {
                e.preventDefault();
                var id = $(this).attr('data-concession');
                await vm.actionShortcut(id, 'issue_concession');
            }).on('click', 'a[data-decline]', async function(e) {
                e.preventDefault();
                var id = $(this).attr('data-decline');
                await vm.actionShortcut(id, 'decline');
            }).on('responsive-display.dt', function () {
                var tablePopover = $(this).find('[data-toggle="popover"]');
                if (tablePopover.length > 0) {
                    tablePopover.popover();
                    // the next line prevents from scrolling up to the top after clicking on the popover.
                    $(tablePopover).on('click', function (e) {
                        e.preventDefault();
                        return true;
                    });
                }
            }).on('draw.dt', function () {
                var tablePopover = $(this).find('[data-toggle="popover"]');
                if (tablePopover.length > 0) {
                    tablePopover.popover();
                    // the next line prevents from scrolling up to the top after clicking on the popover.
                    $(tablePopover).on('click', function (e) {
                        e.preventDefault();
                        return true;
                    });
                }
            });
        },
        initialiseSearch:function(){
            this.dateSearch();
        },
        dateSearch:function(){
            let vm = this;
            vm.$refs.ledgerpay_datatable.table.dataTableExt.afnFiltering.push(
                function(settings,data,dataIndex,original){
                    let from = vm.filterLedgerPayLodgedFrom;
                    let to = vm.filterLedgerPayLodgedTo;
                    let val = original.lodgement_date;

                    if ( from == '' && to == ''){
                        return true;
                    }
                    else if (from != '' && to != ''){
                        return val != null && val != '' ? moment().range(moment(from,vm.dateFormat),moment(to,vm.dateFormat)).contains(moment(val)) :false;
                    }
                    else if(from == '' && to != ''){
                        if (val != null && val != ''){
                            return moment(to,vm.dateFormat).diff(moment(val)) >= 0 ? true : false;
                        }
                        else{
                            return false;
                        }
                    }
                    else if (to == '' && from != ''){
                        if (val != null && val != ''){
                            return moment(val).diff(moment(from,vm.dateFormat)) >= 0 ? true : false;
                        }
                        else{
                            return false;
                        }
                    }
                    else{
                        return false;
                    }
                }
            );
        },

    },
    mounted: function(){
        //this.fetchFilterLists();
        let vm = this;
        $( 'a[data-toggle="collapse"]' ).on( 'click', function () {
            var chev = $( this ).children()[ 0 ];
            window.setTimeout( function () {
                $( chev ).toggleClass( "glyphicon-chevron-down glyphicon-chevron-up" );
            }, 100 );
        });
    },
    updated: function() {
        this.$nextTick(() => {
            this.initialiseSearch();
            this.addEventListeners();
        });
    },
    created: function() {
    },
}
</script>
<style scoped>
</style>
