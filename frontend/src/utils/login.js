

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
