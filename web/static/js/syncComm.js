var character_array = [
    "Miss Scarlet",
    "Col. Mustard",
    "Mrs. White",
    "Mr. Green",
    "Mrs. Peacock",
    "Prof. Plum"
];

var weapon_array = [
    "Revolver",
    "Dagger",
    "Lead Pipe",
    "Rope",
    "Candlestick",
    "Wrench"
];

var location_array = [
    "Study",
    "Hall",
    "Lounge",
    "Library",
    "Billiard Room",
    "Dining Room",
    "Conservatory",
    "Ballroom",
    "Kitchen"
];

var movement_array = [
    "Up",
    "Right",
    "Down",
    "Left",
    "Secret Passage"
];

function selectAnyCharacter() {
    var select = document.getElementById("character_select");
    
    for(var i = 0; i < character_array.length; i++) {
        var opt = character_array[i];
        var el = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        select.appendChild(el);
    }
};

function selectWeapon() {

}

function selectRoom() {
    
}

function getMovement() {
    var select = document.getElementById("move_player");
    
    for(var i = 0; i < movement_array.length; i++) {
        var opt = movement_array[i];
        var el = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        select.appendChild(el);
    }
}

function movePlayer() {

}


