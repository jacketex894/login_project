const BASE_URL = '/api';

export function login(account,password){
    let data = {'account':account,'password':password}
    return fetch(`${BASE_URL}/login`,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
        },
        body:JSON.stringify(data)
    }).then(response =>{
        return response.json();
    })
}

export function register(userData){
    return fetch(`${BASE_URL}/register`,{
        method:'PUT',
        headers:{
            'Content-Type':'application/json',
        },
        body:JSON.stringify(userData),
    }).then(response =>{
        if (!response.ok) {
            throw new Error('error：' + response.status);
        }
        return response.json();
    })
}