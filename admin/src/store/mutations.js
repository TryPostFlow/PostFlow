import Vue from 'vue'


function mutations(types) {
    return {
        [types.SET_ITEMS] (state, payload){
            if(!state.list.hasOwnProperty(payload.request)){
                Vue.set(state.list, payload.request, {})
                Vue.set(state.list[payload.request], 'data', [])
            }
            // Vue.set(state.list[payload.request], 'data', [])
            payload.data.forEach(item => {
                if (item){
                    Vue.set(state.data, item[payload.index], item)
                    if(state.list[payload.request].data.indexOf(item[payload.index]) < 0){
                        state.list[payload.request].data.push(item[payload.index])
                    }
                }
            })
            state.list[payload.request].total = payload.total
            state.list[payload.request].page = payload.page
            state.list[payload.request].page_size= payload.page_size
        },
        [types.SET_ITEM] (state, payload){
            Vue.set(state.data, payload.data[payload.index], payload.data)
        },
        [types.PUSH_ITEM] (state, payload){
            if(!state.list.hasOwnProperty(payload.request)){
                Vue.set(state.list, payload.request, {})
                Vue.set(state.list[payload.request], 'data', [])
            }
            Vue.set(state.data, payload.data[payload.index], payload.data)
            state.list[payload.request].data.push(payload.data)
        },
        [types.DELETE_ITEM] (state, payload){
            Vue.delete(state.data, payload.key)
            Object.keys(state.list).forEach(item => {
                var index = state.list[item].data.indexOf(payload.key)
                if (index != -1){
                    state.list[item].data.splice(index, 1)
                }
            })
        },
    }
}

export default mutations
