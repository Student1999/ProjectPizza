document.addEventListener('DOMContentLoaded',()=>{

  // when users click on the add button, run AddToCart function
  document.querySelectorAll('.add').forEach(button =>{

    addToppings(button);

    // if addtocart button click
    button.onclick = ()=>{
       AddToCart(button);
    }
  });

  //when users click on order button run Order function
  document.querySelector('#order').onclick = ()=>{
    Order();
  }


});
document.addEventListener('click', event => {
        const element = event.target;
        if (element.className === 'overSelect') {
              showCheckboxes(element);
            };


});

// If remove button is clicked, delete the order from database by running RemoveFromCart function.
document.addEventListener('click', event => {
                const element = event.target;
                if (element.className === 'remove') {
                    RemoveFromCart(element);
                    };
});

//send an element to server that user want to add his/her Cart table
function AddToCart(button) {
  const request = new XMLHttpRequest;
  request.open('POST','addtocart');

  request.onload = ()=>{
    const response = JSON.parse(request.responseText);
    const template = Handlebars.compile(document.querySelector('#NewCart').innerHTML);
    meals = JSON.parse(response.meals);
    orders = JSON.parse(response.orders);
    document.querySelector('#NewSelected').innerHTML = '';
    for (var i = 0; i < meals.length; i++) {
      document.querySelector('#NewSelected').innerHTML += template({"meal":meals[i],"order":orders[i]});
    }

  }
    var size = button.parentElement.querySelector('#size').value;
    var order_id = button.parentElement.querySelector('#order_id').value;
    var className = button.parentElement.querySelector('#className').value;
    // to Know what the customer choose for toppings and item.
    let toppings = []
    if (className == 'SicilianPizza' || className == 'RegularPizza') {
      let order_name = button.parentElement.querySelector('#order_name').value;

      button.parentElement.querySelector("#toppings_place").querySelector('#checkboxes').querySelectorAll('input').forEach(input =>{
        if (input.checked) {
          toppings.push(input.value);
        }
      });
  }

  const data = new FormData();
  data.append('order_id',order_id);
  data.append('className',className);
  data.append('size',size);
  data.append('csrfmiddlewaretoken',document.getElementsByName('csrfmiddlewaretoken')[0].value);
  data.append('toppings',toppings);
  request.send(data);
}

// send a message of user to server that they want to make an order
function Order() {

  const request = new XMLHttpRequest;
  request.open('POST','order');

  request.onload = ()=>{
    const response = request.responseText;
    document.querySelector("#NewSelected").innerHTML='';
    document.querySelector("#Selected").innerHTML='';
  }

  const data = new FormData();
  data.append('csrfmiddlewaretoken',document.getElementsByName('csrfmiddlewaretoken')[0].value);
  request.send(data);
}

// send an id to server to remove an item wanted to remove
function RemoveFromCart(button) {
  const request = new XMLHttpRequest;
  request.open('POST','removeItem');

  request.onload = ()=>{
    const response = JSON.parse(request.responseText);
    const template = Handlebars.compile(document.querySelector('#NewCart').innerHTML);
    meals = JSON.parse(response.meals);
    orders = JSON.parse(response.orders);
    document.querySelector('#NewSelected').innerHTML = '';
    for (var i = 0; i < meals.length; i++) {
      document.querySelector('#NewSelected').innerHTML += template({"meal":meals[i],"order":orders[i]});
    }

  }


  let pk = button.parentElement.getElementsByTagName('input')[0].value;

  const data = new FormData();
  data.append('pk',pk);
  data.append('csrfmiddlewaretoken',document.getElementsByName('csrfmiddlewaretoken')[0].value);
  request.send(data);
}

function load_toppings(button,order_name) {
  const request = new XMLHttpRequest;
  request.open('POST','load_toppings');

  request.onload = ()=>{
    const responses = JSON.parse(request.responseText).topping;
    const response = JSON.parse(responses);
    const template = Handlebars.compile(document.querySelector('#Toppings_template').innerHTML);
    button.parentElement.querySelector('#toppings_place').innerHTML = template({"topping":response, "name":order_name});
  }

  const data = new FormData();
  data.append('csrfmiddlewaretoken',document.getElementsByName('csrfmiddlewaretoken')[0].value);
  request.send(data)

}

/////////////////////
var expanded = false;
function showCheckboxes(element) {
  var checkboxes = element.parentElement.parentElement.querySelector("#checkboxes");
  if (!expanded) {
    checkboxes.style.display = "block";
    expanded = true;
  } else {
    checkboxes.style.display = "none";
    expanded = false;
  }
}

//add options to RegularPizza or SicilianPizza that have name topping or item to chose them
function addToppings(button) {
    let size = button.parentElement.querySelector('#size').value;
    let order_id = button.parentElement.querySelector('#order_id').value;
    let className = button.parentElement.querySelector('#className').value;

    if (className == 'SicilianPizza' || className == 'RegularPizza') {
      let order_name = button.parentElement.querySelector('#order_name').value;
      counter = 0;

      for (var i = 2; i < order_name.length; i++) {
        let  name_regular = 'topping';
        let  name_sicilian = 'item';

        if (order_name[i] == name_regular[i-2] || order_name[i] == name_sicilian[i-2] ) {
          counter++;
        }
      }

      if (counter==7 || counter==4) {
          load_toppings(button,order_name);
      }
    }
}
