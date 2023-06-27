var requestOptions = {
    method: 'GET',
    redirect: 'follow'
  };
  
  fetch("http://127.0.0.1:8000/", requestOptions)
    .then(response => response.json())
    .then(data => {
        
    })
    .catch(error => console.log('error', error));