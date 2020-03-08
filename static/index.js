function addEventListenerstoDoc() {
    var elements = document.getElementsByClassName("cards");
    console.log(elements);
    for(var i = 0; i < elements.length; i++){
        console.log(elements[i]);
        suit = elements[i].attributes[1];
        value = elements[i].attributes[2];
        elements[i].addEventListener("click", play_card, false); 
    }
    elem = document.getElementById("cantgobut").addEventListener("click", play_card, false);
}


function play_card(evt){
    console.log(evt.currentTarget.attributes);
    console.log(evt.currentTarget.attributes.length);

    if(evt.currentTarget.attributes.length <= 4){
        var suit = evt.currentTarget.attributes[1];
        var value = evt.currentTarget.attributes[2];
        var cantgo = evt.currentTarget.attributes[3];
    }else{
        var suit = evt.currentTarget.attributes[2];
        var value = evt.currentTarget.attributes[3];
        var cantgo = evt.currentTarget.attributes[4];
    }
    console.log(suit);
    console.log(value);
    const body = {
        card_suit: suit.nodeValue,
        card_value: value.nodeValue,
        cantgo: cantgo.nodeValue
    };
    var url ="/playcard";
    if(document.getElementById("give_card").innerHTML){
        url = '/givecard';
    }
    fetch(url, {
        method: "POST",
        headers: {"Accept": "application/json", "Content-Type": "application/json"},
        credentials: "same-origin",
        body: JSON.stringify(body),
        },
    )
    .then(function(response) {
        /* Check response status code*/
        console.log("%%%%%%%#@#");
        console.log(response);
        CheckResponse(response);
        return response;
    })
    .then(response => response.text())
    .then(result => {
        var parser = new DOMParser();
        var doc = parser.parseFromString(result, 'text/html');
        console.log(doc.body);
        document.body = doc.body;
        addEventListenerstoDoc();
    })
    ;
}


/*
 * Check fetch response status code
 */
function CheckResponse(resp) {
    if (resp.ok) {
        return;
    } else {
        throw new Error("HTTP response not was not OK -> " + resp.status);
    }
}
