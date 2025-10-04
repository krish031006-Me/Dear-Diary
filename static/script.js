// Adding variables to avoid the endless typing
let typingTimeout = null;
let typingId = 0;

// LocalStorage to count the number of times the API has been called
let count = localStorage.getItem('count') || 0;
// Using local storage to store mode
let mode = localStorage.getItem('mode') || 'light';

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
    let title = document.getElementById("title");
    title.style.textAlign = 'center';
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

// A helper delay function
function delay(ms){
    /* here setTimeout will trigger resolve as the delay is over 
        and as soon as resolve is triggered the promise is fulfilled so it will be returned and await will use it */
    return new Promise(resolve => setTimeout(resolve, ms)); 
}

// THis is the function to make Aura the Ai look like typing
async function auraTypes(reflection){
    // Creating the char array
    const reflectArr = reflection.split('');
    // Getting the element
    let box = document.getElementById("AI_box");
    // Now we change the inner HTML with some delay
    for(const char of reflectArr){ // A loop to iterate over every character the array
        box.value += char;
        // calling the helper
        await delay(10);
    }
}

// This is the function to call the flask route
function call_route(){
    // Getting the element
    let entry = document.getElementById("entry_box").value.trim();
    const reflect = document.getElementById('AI_box');

    // can't run anyting with not much content
    if (entry.length < 50) { 
        return;
    }
    
    // --- The Fetch Logic ---
    fetch('/API', { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ entry_text: entry, 
            times: count,
            reflect_text: reflect.value
        })
    })
    .then(response => response.json())
    .then(async(data) => {
        await auraTypes(data.reflection);
        reflect.value +='\n\n';
        // Updating count in localstorage
        count++;
        localStorage.setItem('count', count)
        // Display AI response
        // We use `` for formatted strings in js
    })
    .catch(error => {
        reflect.innerHTML += 'Error contacting AI service.';
        isGood = 0;
        console.error('Fetch Error:', error);
    });
}
 