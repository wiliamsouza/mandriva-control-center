import Qt 4.7
//import QtQuick 1.0

Rectangle {

    property alias text: text.text

    width: 100
    height: 25
    gradient: Gradient {
        GradientStop {
            position: 0
            color: "#e3bdbd"
        }

        GradientStop {
            position: 0.49
            color: "#ac9393"
        }

        GradientStop {
            position: 0.51
            color: "#6c5353"
        }

        GradientStop {
            position: 0.99
            color: "#241c1c"
        }
    }
    clip: true

    Text {
        id: text
        color: "#ffffff"
        text: "Button"
        anchors.centerIn: parent
        //style: Text.Sunken
        font.bold: true
        font.family: "Sans"
    }
}
