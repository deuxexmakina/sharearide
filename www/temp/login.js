// document.getElementById('loginForm').addEventListener('submit', function(event) {
//     // Prevent the default form submit action
//     event.preventDefault();
  
//     // Get the email and password values
//     var email = document.getElementById('email').value;
//     var password = document.getElementById('password').value;
  
//     // Create the login data object
//     var loginData = {
//       email: email,
//       password: password
//     };
  
//   // Send the POST request
//   fetch('http://localhost:5000/login', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     credentials: 'include',  // include credentials in the request
//     body: JSON.stringify(loginData)
//   })
//   .then(response => {
//     if (!response.ok) {
//       throw new Error('Network response was not ok');
//     }
//     return response.json();
//   })
//   .then(data => {
//     if (data.access_token) {
//       document.getElementById('result').textContent = 'Logged in successfully!';
//     } else {
//       document.getElementById('result').textContent = 'Login failed.';
//     }
//   })
//   .catch((error) => {
//     console.error('Error:', error);
//   });
// });


//   // Send the POST request
// fetch('http://localhost:5000/login', {
//   method: 'POST',
//   headers: {
//     'Content-Type': 'application/json'
//   },
//   credentials: 'include'  // include credentials in the request
//   // Your body data here...
// });

document.getElementById('loginForm').addEventListener('submit', function(event) {
  // Prevent the default form submit action
  event.preventDefault();

  // Get the email and password values
  var email = document.getElementById('email').value;
  var password = document.getElementById('password').value;

  // Create the login data object
  var loginData = {
    email: email,
    password: password
  };

  // Log the data to the console for debugging purposes
  console.log(JSON.stringify(loginData));

  // Send the POST request
  fetch('http://localhost:5000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include',  // include credentials in the request
    body: JSON.stringify(loginData)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    if (data.access_token) {
      document.getElementById('result').textContent = 'Logged in successfully!';
    } else {
      document.getElementById('result').textContent = 'Login failed.';
    }
  })
  .catch((error) => {
    console.error('Error:', error);
  });
});
