const BASE_URL = '/expense';

export function create_transaction_record(userData){
    return fetch(`${BASE_URL}/transaction`,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
        },
        body:JSON.stringify(userData)
    }).then(response =>{
        if (!response.ok) {
            throw new Error('error：' + response.status);
        }
        return response.json();
    })
}

export function get_transaction_record(){
    return fetch(`${BASE_URL}/transaction`,{
        method:'GET',
        headers:{
            'Content-Type':'application/json',
        },
    }).then(response =>{
        if (!response.ok) {
            throw new Error('error：' + response.status);
        }
        return response.json();
    })
}