function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', () => {
    let current_orders = new Array();
    let total_price = 0;
    for(order of document.getElementsByClassName('order_price')){
        total_price += parseFloat(order.innerHTML);
    }
    document.getElementById('total_price').innerHTML = total_price;

    for(order of document.getElementsByClassName('orders')){
        current_orders.push(order.id);
    }

    document.querySelector('#place_order').onclick = () => {
    
        const request = new XMLHttpRequest();
        request.open('POST', '/place_order');
        // Callback function for when request completes
        request.onload = () => {
            const data = JSON.parse(request.responseText);

            if (data.success) {
                console.log("Success");
                alert("Ordered Successfully Placed")
                window.location.reload();
            }
            
        }

        const data = new FormData();
        data.append('csrfmiddlewaretoken', csrftoken);
        data.append('current_order_ids', current_orders);
        request.send(data);
        return false;
    };
});