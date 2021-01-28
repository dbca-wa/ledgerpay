<template>
    <div>
        <FormSection :formCollapse="false" label="Payment Item" Index="payment_item">
            <div class="form-group row">
                <label class="col-sm-2">Payment Item</label>
                <div class="col-sm-4">
                    <select class="form-control" v-model="payment_item_selected">
                        <option value=""></option>
                        <option v-for="payment_item in payment_items" :value="payment_item" :key="payment_item.id">
                            <span>
                                {{ payment_item.display_name }}
                            </span>
                        </option>
                    </select>
                </div>
                <div class="col-sm-2 pull-right">
                    <input
                        :disabled="continue_button_disabled"
                        @click="continue_clicked"
                        type="button"
                        value="Continue"
                        class="btn btn-primary"
                    />
                </div>
            </div>
        </FormSection>
        <div v-html="test_contents"></div>
    </div>
</template>

<script>

    import { api_endpoints, helpers }from '@/utils/hooks'
    import FormSection from "@/components/forms/section_toggle.vue"
    import 'bootstrap/dist/css/bootstrap.css';
    import 'eonasdan-bootstrap-datetimepicker';
    import axios from 'axios'

    export default {
        name: 'SectionPaymentItem-section-payment-item-vue',
        props:{

        },
        data:function () {
            let vm = this;
            return {
                payment_items: [],
                payment_item_selected: null,
                test_contents: '',
            }
        },
        components: {
            FormSection,
        },
        watch: {
            payment_item_selected: function(){
                if (!this.payment_item_selected){
                    this.test_contents = ''
                }
            }
        },
        computed: {
            csrf_token: function() {
              return helpers.getCookie('csrftoken')
            },
            continue_button_disabled: function(){
                if (this.payment_item_selected){
                    return false
                } else {
                    return true
                }
            }
        },
        methods:{
            continue_clicked: function(){
                let vm = this;
                window.location = vm.payment_item_selected.api_url
//                axios.get(vm.payment_item_selected.api_url).then(response => {
//                    console.log(response)
//                    vm.test_contents = response.data
//                })
            },
            fetchPaymentItems: function(){
                let vm = this;
                //vm.$http.get('/api/payment_item/list_for_external').then((response) => {
                vm.$http({
                    url: 'http://localhost:8071/api/payment_item/list_for_external',
                    method: 'GET',
                }).then((response) => {
                    console.log(response)
                    vm.payment_items = response.body;
                },(error) => {
                    console.log(error);
                })
            },
            addEventListeners: function() {

            },
        },
        mounted: function() {

        },
        created: function() {
            this.fetchPaymentItems()
        },
    }
</script>

<style lang="css">
    .grow1 {
        flex-grow: 1;
    }
</style>
