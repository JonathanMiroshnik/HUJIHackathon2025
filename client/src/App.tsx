import { useState, useEffect } from 'react'
// import $ from 'jquery';
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [name, setName] = useState("hello");

  // const proxy_request_url = "https://1vp8nl2260.execute-api.us-east-1.amazonaws.com/proxyRequest";

  // function fetchTest() {
  //   fetch(proxy_request_url, {
  //     method: "POST",
  //     headers: {
  //       "Content-Type": "application/json"
  //     },
  //     body: JSON.stringify({
  //       command: "proxy_request_test",
  //       params: "code=testcode!"
  //     })
  //   })
  //   .then(response => response.json())
  //   .then(data => {
  //     console.log("Response from Lambda:", data);
  //   })
  //   .catch(error => {
  //     console.error("Error calling Lambda:", error);
  //   });
  // }

  // const makeAjaxCall = () => {
  //   $.ajax({
  //     url: proxy_request_url,
  //     type: 'POST',
  //     contentType: 'application/json',
  //     data: JSON.stringify({
  //       command: 'proxy_request_test',
  //       params: 'code=testcode!'
  //     }),
  //     success: function(data) {
  //       console.log('AJAX Success:', data);
  //       // Handle successful response
  //     },
  //     error: function(xhr, status, error) {
  //       console.error('AJAX Error:', status, error);
  //       // Handle error
  //     }
  //   });
  // };

  useEffect(() => {
    fetch("http://localhost:8000/api")
      .then((res) => res.json())
      .then((data) => console.log(setName(data.message)))
      .catch((err) => console.error("Error fetching:", err));
    
    // fetchTest();
    // makeAjaxCall();
  }, []);


  // const handleUnload = () => {
    
  // };

  // window.addEventListener('beforeunload', handleUnload);


  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button>
          count is {name}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
