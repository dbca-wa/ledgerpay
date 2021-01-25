import LedgerPayForm from '../../ledgerpay_form.vue'
export default
{
    path: '/external',
    component:
    {
        render(c)
        {
            return c('router-view')
        }
    },
    children: [
        {
            path: '/',
            component: LedgerPayForm,
            name: 'external-ledgerpay-form'
        },
    ]
}
