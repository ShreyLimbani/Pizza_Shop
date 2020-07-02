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


var pizza_id = 0;
var price = [0.00,0.00,0.00];

function add_topping() {
    for (topping of toppings){
        const current_price = topping.value;
        let current_state = topping.checked;
        topping.onchange = () => {
            if (current_state == false){
                current_state = true;
                document.getElementById('order_total').innerHTML = parseFloat(document.getElementById('order_total').innerHTML) + parseFloat(current_price);
            }
            else{
                current_state = false;
                document.getElementById('order_total').innerHTML = parseFloat(document.getElementById('order_total').innerHTML) - parseFloat(current_price);
            }
        };
    }
}

document.addEventListener('DOMContentLoaded', () => {
    let pizzas = document.getElementsByClassName('add_to_cart');
    for (pizza of pizzas){
            const current_pizza_id = pizza.parentElement.id;
            const current_price = [0.00,0.00,0.00];
            current_price[0] = parseFloat(document.getElementById(current_pizza_id+'_small_price').innerHTML.slice(1));
            current_price[1] = parseFloat(document.getElementById(current_pizza_id+'_medium_price').innerHTML.slice(1));
            current_price[2] = parseFloat(document.getElementById(current_pizza_id+'_large_price').innerHTML.slice(1));

        pizza.onclick = () => {
            console.log(current_pizza_id);
            pizza_id = current_pizza_id;
            price = current_price;
            document.getElementById('Medium').checked = true;
            document.getElementById('order_total').innerHTML = price[1];
            document.getElementById('modalSmallPrice').innerHTML = price[0];
            document.getElementById('modalMediumPrice').innerHTML = price[1];
            document.getElementById('modalLargePrice').innerHTML = price[2];
        }; 
    }

    sizes = document.getElementsByClassName('size');
    toppings = document.getElementsByClassName('toppings');

    for (size of sizes){ 
        const current_size = size.value;
        size.onchange = () => {
            document.getElementById('order_total').innerHTML = price[parseInt(current_size)];
            for (topping of toppings){
                topping.checked = false;
            }
            add_topping();
        };
    }
    
    add_topping();

    document.querySelector('#add_to_cart').onsubmit = () => {

        // Initialize new request
        const request = new XMLHttpRequest();
        const pizza_size = "Medium";
        let pizza_toppings = new Array();
        const pizza__total_price = document.getElementById('order_total').innerHTML;
        sizes = document.getElementsByClassName('size');
        toppings = document.getElementsByClassName('toppings');
        
        for(size in sizes){
            if(size.checked == true){
                pizza_size = size.id;
            }
        }
        
        for(topping of toppings){
            if(topping.checked == true){
                pizza_toppings.push(topping.id);
            }
        }
        if (pizza_toppings.length == 0)
        {
            pizza_toppings.push(0);
        }
        request.open('POST', '/add-pizza');

        // Callback function for when request completes
        request.onload = () => {
            const data = JSON.parse(request.responseText);

              if (data.success) {
                  console.log("Success");
                  window.location.reload();
              }
            
        }

        // Add data to send with request
        const data = new FormData();
        data.append('csrfmiddlewaretoken', csrftoken);
        data.append('pizza_id', pizza_id);
        data.append('pizza_size', pizza_size);
        data.append('pizza_toppings', pizza_toppings);
        data.append('pizza_total', pizza__total_price);

        // Send request
        request.send(data);
        return false;
    };

});