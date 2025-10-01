// Adding variables to avoid the endless typing
let typingTimeout = null;
let typingId = 0;

// This is DOMContentLoaded event and will be used to call all the necessary functions
document.addEventListener("DOMContentLoaded", function(event){

    // Calling the function only if there is a title id element present i.e only on dashboard
    if(document.getElementById("title")){
        // Calling the type_title() function
        title_type();
    } 
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