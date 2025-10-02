// Adding variables to avoid the endless typing
let typingTimeout = null;
let typingId = 0;

// LocalStorage to count th enumber of times the API has been called
let count = localStorage.getItem('count') || 0;

// A global flag to prevent error full API calls
let isGood=1;

/* This is the debounce function-
    This function let's us effectively call a specific function
    after a single time condition is met*/
function debounce(func, delay = 500) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
}

// This is DOMContentLoaded event and will be used to call all the necessary functions
document.addEventListener("DOMContentLoaded", function(event){

    // Calling the function only if there is a title id element present i.e only on dashboard
    if(document.getElementById("title")){
        // Calling the type_title() function
        title_type();
    } 

    // Checking if we are on the space page to run the control function
    const inputField = document.getElementById("entry_box");
    // Calling when it exists and the inner HTML is greater than 50 characters
    if(inputField && isGood === 1){
        // Calling the debouncer to run call_route when the user doen't press anything fro 8 sec straight
        const debouncedCall = debounce(call_route, 8000);
        inputField.addEventListener('input', debouncedCall);
    }   
});

// This is the eventlistener to delete coount from storage beofre unloading
window.addEventListener("beforeunload", function(event){
    // removing the item from localstorage
    localStorage.removeItem("count")
});

// The typing function for title
function title_type(){

    if (typingTimeout){
        clearTimeout(typingTimeout);
        typingTimeout = null;
    }
    typingId++;
    const myrun = typingId;
    // Variables that would be used later-
    word_count = 0;
    letter_count = 0;

    // The text to be typed in an array
    let title_text = ["dear", "Diary"];
    // The first and second word  of the element
    let first = document.getElementById("first_word");
    let second = document.getElementById("second_word");
    if (first){
        first.innerHTML = "";
    }
    if (second){
        second.innerHTML = "";
    }
    // the actual typing function
    function type(){
        // checking to avoid multiple typing animations
        if(myrun != typingId){
                typingTimeout = null;
                return;
            }

        // an escape sequence
        if (word_count >= title_text.length){
            typingTimeout = null;
            return;
        }
        
        // The actual typing begins
        if (letter_count < title_text[word_count].length){
            if (word_count === 0){
                first.innerHTML += title_text[word_count][letter_count];
            }
            else if (word_count === 1){
                second.innerHTML += title_text[word_count][letter_count];
            }
            letter_count++;
        }
        else{
            word_count++;
            letter_count = 0;
        }
        typingTimeout = setTimeout(type, 200);
    }
    type();
};

// This is the function to call the flask route
function call_route(){
    // Getting the element
    let entry = document.getElementById("entry_box").value.trim();
    let reflect = document.getElementById('AI_box').value.trim();

    // can't run anyting with not much content
    if (entry.length < 50) { 
        return;
    }
    
    // --- The Fetch Logic ---
    fetch('/', { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ entry_text: entry, 
            times: count,
            reflect_text: reflect
        })
    })
    .then(response => response.json())
    localStorage.setItem('count', count + 1)
    .then(data => {
        // Display AI response
        // We use `` for formatted strings in js
        reflection.innerHTML += `<p>${data.reflection}</p>`;
    })
    .catch(error => {
        reflection.innerHTML += 'Error contacting AI service.';
        isGood = 0;
        console.error('Fetch Error:', error);
    });
}
