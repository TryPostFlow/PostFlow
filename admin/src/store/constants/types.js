
function create_types(type){
    return {
        FETCH_ITEMS: `${type}/FETCH_ITEMS`,
        FETCH_ITEM: `${type}/FETCH_ITEM`,
        CREATE_ITEM: `${type}/CREATE_ITEM`,
        UPDATE_ITEM: `${type}/UPDATE_ITEM`,
        SET_ITEMS: `${type}/SET_ITEMS`,
        SET_ITEM: `${type}/SET_ITEM`,
        PUSH_ITEM: `${type}/PUSH_ITEM`,
        GET_ITEMS: `${type}/GET_ITEMS`,
        GET_ITEM: `${type}/GET_ITEM`,
        DELETE_ITEM: `${type}/DELETE_ITEM`,
    }
}

export default create_types