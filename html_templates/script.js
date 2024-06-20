document.addEventListener("DOMContentLoaded", function() {
    const settingsIcon = document.getElementById('settings-icon');
    const settingsMenu = document.getElementById('settings-menu');

    // Toggle settings menu visibility on settings icon click
    settingsIcon.addEventListener('click', function() {
        settingsMenu.classList.toggle('show');
    });

    // Close the settings menu if user clicks outside of it or clicks an option
    document.addEventListener('click', function(event) {
        if (!settingsMenu.contains(event.target) && event.target !== settingsIcon) {
            settingsMenu.classList.remove('show');
        }
    });

    // Close the settings menu when clicking on an option
    settingsMenu.addEventListener('click', function(event) {
        // Check if the clicked target is an anchor tag within settings-menu
        if (event.target.tagName === 'A') {
            settingsMenu.classList.remove('show');
        }
    });
});

function vibrateButton(button) {
    button.style.animation = "vibrate 0.2s infinite";
    setTimeout(() => {
        button.style.animation = "";
    }, 1000);
}























// function vibrateButton(button) {
//     button.style.animation = "vibrate 0.2s infinite";
//     setTimeout(() => {
//         button.style.animation = "";
//     }, 1000);
// }

// document.addEventListener("DOMContentLoaded", function() {
//     const settingsIcon = document.getElementById('settings-icon');
//     const settingsMenu = document.getElementById('settings-menu');

//     // Toggle settings menu visibility on settings icon click
//     settingsIcon.addEventListener('click', function() {
//         settingsMenu.classList.toggle('show');
//     });

//     // Close the settings menu if user clicks outside of it
//     document.addEventListener('click', function(event) {
//         if (!settingsMenu.contains(event.target) && event.target !== settingsIcon) {
//             settingsMenu.classList.remove('show');
//         }
//     });
// });


// // // CSS keyframes for vibration
// // const style = document.createElement('p2');
// // style.innerHTML = `
// // @keyframes vibrate {
// //     0% { transform: translate(1px, 1px) rotate(0deg); }
// //     10% { transform: translate(-1px, -2px) rotate(-1deg); }
// //     20% { transform: translate(-3px, 0px) rotate(1deg); }
// //     30% { transform: translate(3px, 2px) rotate(0deg); }
// //     40% { transform: translate(1px, -1px) rotate(1deg); }
// //     50% { transform: translate(-1px, 2px) rotate(-1deg); }
// //     60% { transform: translate(-3px, 1px) rotate(0deg); }
// //     70% { transform: translate(3px, 1px) rotate(-1deg); }
// //     80% { transform: translate(-1px, -1px) rotate(1deg); }
// //     90% { transform: translate(1px, 2px) rotate(0deg); }
// //     100% { transform: translate(1px, -2px) rotate(-1deg); }
// // }
// // `;
// document.head.appendChild(style);
