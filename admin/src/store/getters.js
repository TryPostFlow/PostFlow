function getters (types){
    return {
        [types.GET_ITEMS]: (state) => (request) =>{
            request = request?request:'default'
            if(state.list.hasOwnProperty(request)){
                return {
                    data: state.list[request].data.map(id => state.data[id]).filter(_=>_),
                    total: state.list[request].total,
                    page: state.list[request].page,
                    page_size: state.list[request].page_size
                }
            }
            return []
        },
        [types.GET_ITEM]: (state) =>(id) =>{
            return state.data[id]
        }
    }
}

export default getters