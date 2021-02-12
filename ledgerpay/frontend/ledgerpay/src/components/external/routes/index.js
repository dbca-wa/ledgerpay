import LedgerPayForm from '../external_home.vue'
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
