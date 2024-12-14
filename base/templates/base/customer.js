// Sample data arrays
let customers=[];
let serviceRequests=[];
let subscriptions=[];

// DOM elements
const customerForm = document.getElementById("customerForm");
const serviceRequestForm = document.getElementById("serviceRequestForm");
const subscriptionForm = document.getElementById("subscriptionForm");
const statusFilter = document.getElementById("statusFilter");

// Event Listeners
customerForm.addEventListener("submit", addCustomer);
serviceRequestForm.addEventListener("submit", addServiceRequest);
subscriptionForm.addEventListener("submit", updateSubscription);
statusFilter.addEventListener("change", filterCustomers);

// Add Customer Function
function addCustomer(event) {
    event.preventDefault();
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const status = document.getElementById("status").value;

    const customer = {
        name,
        email,
        phone,
        status
    };

    customers.push(customer);
    renderCustomerList();
    customerForm.reset();
}

// Add Service Request Function
function addServiceRequest(event) {
    event.preventDefault();
    const customerName = document.getElementById("requestCustomer").value;
    const requestDetails = document.getElementById("requestDetails").value;

    const request = {
        customerName,
        requestDetails
    };

    serviceRequests.push(request);
    renderServiceRequests();
    serviceRequestForm.reset();
}

// Update Subscription Function
function updateSubscription(event) {
    event.preventDefault();
    const customerName = document.getElementById("subscriptionCustomer").value;
    const subscriptionStatus = document.getElementById("subscriptionStatus").value;

    const subscription = {
        customerName,
        subscriptionStatus
    };

    subscriptions.push(subscription);
    renderSubscriptionInfo();
    subscriptionForm.reset();
}

// Render Customer List
function renderCustomerList() {
    const customerProfiles = document.getElementById("customerProfiles");
    customerProfiles.innerHTML = '';
    const filterValue = statusFilter.value;

    customers
        .filter(customer => !filterValue || customer.status === filterValue)
        .forEach(customer => {
            const customerCard = document.createElement("div");
            customerCard.classList.add("customer-card");
            customerCard.innerHTML = `
                <h3>${customer.name}</h3>
                <p>Email: ${customer.email}</p>
                <p>Phone: ${customer.phone}</p>
                <p>Status: ${customer.status}</p>
            `;
            customerProfiles.appendChild(customerCard);
        });
}

// Render Service Requests
function renderServiceRequests() {
    const serviceRequestsContainer = document.getElementById("serviceRequests");
    serviceRequestsContainer.innerHTML = '';

    serviceRequests.forEach(request => {
        const requestCard = document.createElement("div");
        requestCard.classList.add("customer-card");
        requestCard.innerHTML = `
            <h3>Service Request for ${request.customerName}</h3>
            <p>${request.requestDetails}</p>
        `;
        serviceRequestsContainer.appendChild(requestCard);
    });
}

// Render Subscription Info
function renderSubscriptionInfo() {
    const subscriptionInfo = document.getElementById("subscriptionInfo");
    subscriptionInfo.innerHTML = '';

    subscriptions.forEach(subscription => {
        const subscriptionCard = document.createElement("div");
        subscriptionCard.classList.add("customer-card");
        subscriptionCard.innerHTML = `
            <h3>Subscription for ${subscription.customerName}</h3>
            <p>Status: ${subscription.subscriptionStatus}</p>
        `;
        subscriptionInfo.appendChild(subscriptionCard);
    });
}

// Filter Customers by Status
function filterCustomers() {
    renderCustomerList();
}

s