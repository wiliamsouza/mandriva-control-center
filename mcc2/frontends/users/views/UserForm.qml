//import Qt 4.7
import QtQuick 1.0

// ** Not used variable scope problem **

Grid {
    columns: 2
    spacing: 12
    //anchors.left: parent.left
    anchors.leftMargin: 12
    //anchors.top: parent.top
    anchors.topMargin: 12

    // Line #1
    Text {
        text: "Full name:"
        color: "black"
        opacity: 0.6
        font.bold: true
        font.pixelSize: 15
    }
    TextInput {
        id: fullName
        width: 215
        text: "full name"
        focus: true
        selectByMouse: true
    }

    // Line #2
    Text {
        text: "Login:"
        color: "black"
        opacity: 0.6
        font.bold: true
        font.pixelSize: 15
    }
    TextInput {
        id: login
        width: 215
        text: "login"
        focus: true
        selectByMouse: true
    }

    // Line #3
    Text {
        text: "Password:"
        color: "black"
        opacity: 0.6
        font.bold: true
        font.pixelSize: 15
    }
    TextInput {
        id: password
        width: 215
        text: "password"
        focus: true
        selectByMouse: true
    }

    // Line #4
    Text {
        text: "Confirm password:"
        color: "black"
        opacity: 0.6
        font.bold: true
        font.pixelSize: 15
    }
    TextInput {
        id: confirmPassword
        width: 215
        text: "confirm password"
        focus: true
        selectByMouse: true
    }

    // Line #5
    Text {
        text: "Login shell:"
        color: "black"
        opacity: 0.6
        font.bold: true
        font.pixelSize: 15
    }
    TextInput {
        id: loginShell
        width: 215
        text: "login shell"
        focus: true
        selectByMouse: true
    }

    // Line #6
    Text {
        text: "Home:"
        color: "black"
        opacity: 0.6
        font.bold: true
        font.pixelSize: 15
    }
    TextInput {
        id: home
        width: 215
        text: "home"
        focus: true
        selectByMouse: true
    }
}
