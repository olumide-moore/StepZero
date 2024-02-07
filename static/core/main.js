
//Hamburger menu
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});
//Ensure that the hamburger menu is hidden when a menu item is clicked
const menuLinks = document.querySelectorAll('.nav-link');
menuLinks.forEach((menuLink) => {
    menuLink.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});


//Postcode completed typing
var typingTimer;
var doneTypingInterval = 500;
var postcode = document.getElementById('postcode');
var addressList = document.getElementById('address');

postcode.addEventListener('keyup', function () {
    clearTimeout(typingTimer);
    if (postcode.value) { //if the input isn't empty, start the timer and validate the postcode after the interval
        typingTimer = setTimeout(fetchAddressess(postcode.value), doneTypingInterval); 
    }
});
postcode.addEventListener('keydown', function () {
    clearTimeout(typingTimer); //reset the timer
});

function validatePostcode(postcodeValue) {
    //    let postcodeValue = postcode.value.trim();
    postcodeValue = postcodeValue.replace(/\s+/g, ''); //remove any spaces
    if (/^[A-Z]{1,2}[0-9]{1,2} ?[0-9][A-Z]{2}$/i.test(postcodeValue)) {
        console.log(postcodeValue);
        //add space to the postcode ccounting from the right
        postcodeValue = postcodeValue.slice(0, -3) + ' ' + postcodeValue.slice(-3);
        postcodeValue = postcodeValue.toUpperCase();
        return postcodeValue;
    }
    return '';
}
function fetchAddressess(postcodeValue) {
    addressList.innerHTML = '';
    postcodeValue = validatePostcode(postcodeValue);
    if (postcodeValue) {
        fetch(`/getaddresses/?&postcode=${postcodeValue}`)
            .then(response => response.json()).then(data => {
                if (data.addresses) {
                    putAddresses(data.addresses);
                }else if (data.error) {
                    console.log(data.error);
                }
            }).catch(error => {
                console.error('Error fetching data:', error)});    
    }  
}


function putAddresses(addresses) {
    addressList.innerHTML = '';
    addresses.forEach(address => {
        let option = document.createElement('option');
        option.value = address;
        option.text = address;
        addressList.appendChild(option);
    });
}

function step2Clicked(event) {
    let addressValue = addressList.value;
    console.log(addressValue);
    if (addressValue) {
        fetch(`/step2/?address=${addressValue}`)
            .then(response => response.json()).then(data => {
                console.log("data");
            }).catch(error => {
                console.error('Error fetching data:', error)});    
    }
    // postcodeValue 
    // if (postcode.value) {
    // fetchData();
}


// fetchAddressess("SE11 5JH");
// //Fetch addresses from the postcode
// async function fetchAddressess(postcode) {
//     let url = `https://epc.opendatacommunities.org/api/v1/non-domestic/search`;
//     let email = `olumide.moore2817@gmail.com`;
//     let api_key = `51dae8b5fb342c818d4659f3ee600ac383d77403`;
//     let headers = {
//         // 'Content-Type': 'application/json',
//         'Authorization': 'Basic ' + btoa(email + ':' + api_key)
//     }
    
//     let page = 1;
//     let limit = 100;

//     url = `${url}?page=${page}&limit=${limit}&postcode=${postcode}`;
//     // fetch(url, {
//     //     method: 'GET',
//     //     headers: headers
//     // }).then(response => response).then(data => {
//     //     console.log(data);
//     // }).catch(error => {
//     //     console.log(error);
//     // });
//       const response = await fetch(url, { headers: headers });

//       if (response.ok) {
//         const data = await response;
//         console.log(data);
//       }

// }