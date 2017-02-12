import axios from './constants/api'

function actions(types){
    return {
        [types.FETCH_ITEMS] ({commit, state}, {path, params, request, index}){
            params = params || {}
            return axios.get(path, {params: params})
                .then(function (response) {
                    commit(types.SET_ITEMS, {
                        request: request?request:'default',
                        index: index?index:'id',
                        data: response.data,
                        total:'x-total' in response.headers?parseInt(response.headers['x-total']):0,
                        page: 'x-page' in response.headers?parseInt(response.headers['x-page']):0,
                        page_size: 'limit' in params?params['limit']:20
                    })
                })
        },
        [types.FETCH_ITEM] ({commit, state}, {path, params, index}){
            // path: `posts/${param['id']}`
            return axios.get(path)
                .then(function (response) {
                    commit(types.SET_ITEM, {
                        index: index?index:'id',
                        data: response.data
                    })
                })
        },
        [types.CREATE_ITEM] ({commit, state}, {path, params, request, index}){
            // path: `posts`
            return new Promise((resolve, reject) => {
                axios.post(path, params)
                .then(function (response) {
                    commit(types.PUSH_ITEM, {
                        request: request?request:'default',
                        index: index?index:'id',
                        data: response.data
                    })
                    resolve(response)
                })
                .catch(function (error) {
                    reject(error);
                });
            })
        },
        [types.UPDATE_ITEM] ({commit, state}, {path, params, request, index}){
            // path: `posts/${param['id']}`
            return axios.put(path, params)
                .then(function (response) {
                    if(response.data instanceof Array){
                        commit(types.SET_ITEMS, {
                            request: request?request:'default',
                            index: index?index:'id',
                            data: response.data,
                            total:'x-total' in response.headers?parseInt(response.headers['x-total']):0,
                            page: 'x-page' in response.headers?parseInt(response.headers['x-page']):0,
                            page_size: 'limit' in params?params['limit']:20
                        })
                    }else{
                        commit(types.SET_ITEM, {
                            index: index?index:'id',
                            data: response.data
                        })
                    }
                })
        },
        [types.DELETE_ITEM]({commit, state}, {path, params}){
            // path: `posts/${param['id']}`
            return axios.delete(path)
                .then(function (response) {
                    commit(types.DELETE_ITEM, {
                        key: params.key,
                    })
                })
        }
    }
}

export default actions
