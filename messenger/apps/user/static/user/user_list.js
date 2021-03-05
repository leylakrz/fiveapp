var cash = []
var suggestions = document.querySelector('.sug');

var email = document.getElementsByTagName('input')[1];
email.addEventListener('input', (event) => {
    clear_sug()
    var email_input_length = event.target.value.length
    if (email_input_length > 2) {
        if (email_input_length === 3) {
            $.getJSON('http://127.0.0.1:8000/emails/?input=' + event.target.value, function (data) {
                cash = data;
                check_cash(cash, event.target.value)
            })
        } else {
            check_cash(cash, event.target.value)
        }


    } else {
        add_sug('enter at least 3 chars.');
    }
})

function clear_sug() {
    while (suggestions.firstChild) {
        suggestions.removeChild(suggestions.firstChild);
    }
}

function check_cash(cash, input) {
    if (cash.length > 0) {
        var sug_found = false;
        for (var i = 0; i < cash.length; i++) {
            if (cash[i]['email'].search(input) > -1) {
                add_sug(cash[i]['email']);
                sug_found = true;
            }
        }
        if (!sug_found) {
            add_sug('no result.');
        }

    } else {
        add_sug('no result.');
    }
}

function add_sug(content) {
    var div = document.createElement('DIV')
    div.innerText = content
    suggestions.appendChild(div)

    if (content !== 'no result.') {
        div.addEventListener('click', (event) => {
            email.value = content
        })
    }
}

