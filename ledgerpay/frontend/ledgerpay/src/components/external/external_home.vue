<template>
    <div class="container">
        <SectionPaymentItem />
    </div>
</template>

<script>

    import { api_endpoints, helpers }from '@/utils/hooks'
    import FormSection from "@/components/forms/section_toggle.vue"
    import SectionPaymentItem from "@/components/common/section_payment_item"
    import 'bootstrap/dist/css/bootstrap.css';
    import 'eonasdan-bootstrap-datetimepicker';

    export default {
        name: 'ExternalHome-external-home-vue',
        props:{

        },
        data:function () {
            let vm = this;
            return {

            }
        },
        components: {
            SectionPaymentItem,
        },
        watch: {

        },
        computed: {
            csrf_token: function() {
              return helpers.getCookie('csrftoken')
            },
        },
        methods:{
            addEventListeners: function() {

            },
        },
        mounted: function() {

        },
        created: function() {

        },
    }
</script>

<style lang="css">

</style>
